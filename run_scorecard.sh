#!/bin/ksh
### This script is used to create the EMC Verification Scorecard.
### An html graphic is uploaded to the web at the end of this script.
### Users must run vsdbjob_submit.sh first with create maps set (MAKEMAPS=YES) 
### for the scorecard text files to be created which are read by this script.
### Users should only need to change the 9 variables at the top of this script.
### Written by: DaNa Carlis and Rebecca LaPorta 11/5/2013
### May 2013: Updated statistical significane creteria by Fanglin Yang and DaNa Carlis. 

#=============================================================================
# Functione Name :
#    GetVar
#
# Usage :
#    GetVar $var
#
# Description :
#    Look up variable from configuration file and print out its value
#
# Process Description :
#     Check number of arguments
#
# Data Files :
#    $CFG_FL file
#
# Restriction :
#    1. $FG_FL file must exist
#    2. the variable format of the file must be "variable=value"
#    3. if the line first is "#" ==> it will be to ignore
# Date :
#    Jan 05, 2005
#=========================================================================
GetVar()
{
  typeset Arg_V
  Arg_V=$1
  if [ "${Arg_V}" ] ; then
     Var_value=$(grep "${Arg_V}=" ${CFG_FL} | grep -v "^#" | cut -d= -f2)
    if [ "${Var_value}" ] ; then
      echo ${Var_value}
    fi
  fi
}


#set -x
export SDATE=${DATEST:-2014010100}
export EDATE=${DATEND:-2014011500}
export mdlist=${mdlist:-"gfs ecm"}                     ;#Can only compare 2 experiments 
export webhostid=${webhostid:-""}              ;#login id on rzdm webhost
export webhost=${webhost:-""}     ;#login id on webhost
export ftpdir=${ftpdir:-""}  ; #where maps are  displayed
export mapdir=${mapdir:-/stmpd2/$LOGNAME/nwpvrfy/web}  ; #place to save output in local machine 
export doftp=${doftp:-"NO"}                           ; #whether or not sent html files to scardftp 
export caplist=${caplist:-$mdlist}                     ;#caption lis

#Calculate total number of days
vsdbhome=${vsdbhome:-/home/xa38/GVER}
y1=`echo $SDATE |cut -c 1-4 `
m1=`echo $SDATE |cut -c 5-6 `
d1=`echo $SDATE |cut -c 7-8 `
y2=`echo $EDATE   |cut -c 1-4 `
m2=`echo $EDATE   |cut -c 5-6 `
d2=`echo $EDATE   |cut -c 7-8 `
ndays=`${vsdbhome}/map_util/days.sh -a $y2 $m2 $d2 - $y1 $m1 $d1`
export ndays=`expr $ndays + 1 `
CFG_FL=${vsdbhome}/etc/makescorecard.cfg

#User can find the location of scorecard text files from vsdbjob_submit.sh
scoredir=${scoredir:-$rundir/score}                    ; #location of scard text files
mkdir -p $scoredir
cd $scoredir || exit
echo $scoredir
#Undefined value
undef=-9999.0
#--------------------------------------------------------------------
## -- Users should not have to change any of the parameters below--##
## -- verification parameters
export statlist=${statlist:-"cor rms bias"}
export reglist=${reglist:-"G2 G2PNA G2NHX G2SHX G2TRO"}
export day=${day4card:-"1 3 5 6 8"}
ndd=`echo $day |wc -w`

#Verification scorecard html filename
htfile=scorecard.html
legfile=legend.html
mainfile=mainindex.html
cssfile=scorecard.css
rm -f $htfile $legfile $mainfile $cssfile

#Create Header for HTML FILE
print $htfile
cat <<EOF >> $htfile
<link type="text/css" rel="stylesheet" href="scorecard.css"/>
<table class="first" cellpadding="0.2">
 <tbody align="center">
  <!--Regions-->
  <tr>
   <th></th>
   <th></th>
   <th></th>
EOF

for reg1 in $reglist; do
  title=$(GetVar ${reg1}_title)
  world=$(echo "<th colspan=$ndd >${title}</th>")

cat <<EOF >> $htfile
    $world
EOF
done

cat <<LSF >> $htfile
  </tr>
  <!--Days-->
   <tr>
    <td></td>
    <td></td>
    <td></td>
LSF

#How many regions will be displayed on scorecard
regcount=`echo $reglist |wc -w`
ct=1
while [[ $ct -le $regcount ]]; do

i=1
for pday in $day; do
  flag=`echo ${i} | awk '{ print $1%2 }'` 
  if [[ ${flag} -eq 1 ]]; then
     sday=$(echo '<td>Day '${pday}'</td>')
  elif [[ ${flag} -eq 0 ]]; then
     sday=$(echo '<td style="background:#E6E6E6">Day '${pday}'</td>')
  fi   

  i=$(( $i + 1 ))
cat <<LSF >> $htfile
    $sday
LSF
 done
 ct=$(( $ct + 1 ))
done #End of while loop

cat <<EOF >> $htfile
   </tr>
EOF


set -A mdname $caplist
mdnamec1=$(echo ${mdname[0]} |tr "[a-z]" "[A-Z]") 
mdnamec2=$(echo ${mdname[1]} |tr "[a-z]" "[A-Z]") 

echo ${mdnamec1}
echo ${mdnamec2}


count_tmp=$(\pwd | awk '{ print $1"/count.tmp"}')
if [ -e "${count_tmp}" ] ; then rm -f ${count_tmp} ; fi

for stat in $statlist ; do  #Loop over cor, rms, bias
  stat_count="0"
  statname=$(GetVar ${stat}_name)
  vnamlist=$(GetVar ${stat}_var)
  for var in $vnamlist ; do
    lev=$(GetVar ${stat}_${var}_level)
    lev_count=$(echo ${lev} | wc -w)
    stat_count=$(echo ${stat_count} ${lev_count} | awk '{ print $1+$2 }')
    echo "rspan|${stat}|${var}|${lev_count}" >> ${count_tmp}
  done
  echo "statspan|${stat}|${stat_count}" >> ${count_tmp}
done


for stat in $statlist ; do 
  statname=$(GetVar ${stat}_name)
  vnamlist=$(GetVar ${stat}_var)
  statspan=`grep "statspan|${stat}" ${count_tmp} | awk -F"|" '{ print $3 }'` 

cat <<EOF >> $htfile
   <tr>
    <th id="thside" rowspan="$statspan">$statname</th>
EOF

for vnam in $vnamlist ; do #Loop over HGT, T, U, V, WIND
  rspan=`grep "rspan|${stat}|${vnam}" ${count_tmp} | awk -F"|" '{ print $4 }'` 
  vname=$(GetVar ${stat}_${vnam}_name)
  levlist=$(GetVar ${stat}_${vnam}_level)
cat <<EOF >> $htfile
     <td rowspan="${rspan}">$vname</td>
EOF



for lev in $levlist ; do  #Loop over P1000, P500, P250mlist 

  if [[ $lev = "P1000" ]] ; then
    lev1=$(echo $lev |cut -c 2-5)
  else
    lev1=$(echo $lev |cut -c 2-4)
  fi

  if [[ $vnam = "PMSL" ]] ; then
    lev1=$lev
cat <<EOF >> $htfile
     <td>${lev1}</td>
EOF
  else
cat <<EOF >> $htfile
     <td>${lev1}hPa</td> 
EOF
  fi
for reg in $reglist ; do  #Loop over G2, NH, SH

for dd in $day ; do      #Loop over day 1,3,5,6,8,10

namedaily=${vnam}_${lev}_${reg}

file1=${scoredir}/score_${stat}_${namedaily}_${mdnamec1}_day${dd}.txt
file2=${scoredir}/score_${stat}_${namedaily}_${mdnamec2}_day${dd}.txt
file3=${scoredir}/score_${stat}_conflimit_${namedaily}_${mdnamec2}_day${dd}.txt

if [[ ! -s "$file1" || ! -s "$file2" || ! -s "$file3" ]] ; then
  echo "All text files do not exist to create verif scorecard" 
  echo "Check that all files exist and have size"
  echo "Check file1: " $file1
  ls - $file1
  echo "Check file2: " $file2
  ls - $file2
  echo "Check file3: " $file3
  ls - $file3
  sym=$(echo '<td style="background:#58ACFA"></td>')
cat <<EOFF >> $htfile
       $sym
EOFF
#  exit 
else

#Set default score
score1=$undef
score2=$undef
conf1=$undef

while read line          
do           
score1=$(echo $line | awk '{print $1}' | bc)
done < ${file1}
while read line
do
score2=$(echo $line | awk '{print $1}' | bc)
done < ${file2}
while read line
do
conf1=$(echo $line | awk '{print $1}' | bc)
done < ${file3}

if [[ $ndays -ge 80 ]] ;then
  alpha1=1.960  ; #95% confidence level
  alpha2=2.576  ; #99% confidence level
  alpha3=3.291  ; #99.9% confidence level
elif [[ $ndays -ge 40 && $ndays -lt 80 ]] ;then
  alpha1=2.0    ; #95% confidence level
  alpha2=2.66   ; #99% confidence level
  alpha3=3.46   ; #99.9% confidence level
elif [[ $ndays -ge 20 && $ndays -lt 40 ]] ;then
  alpha1=2.042  ; #95% confidence level
  alpha2=2.75   ; #99% confidence level
  alpha3=3.646  ; #99.9% confidence level
elif [[ $ndays -lt 20 ]] ; then
  alpha1=2.228  ; #95% confidence level
  alpha2=3.169  ; #99% confidence level
  alpha3=4.587  ; #99.9% confidence level
fi

if [[ $score1 == $undef || $score2 == $undef || $conf1 == $undef ]] ; then
  ds=$undef
else
  if [[ $stat = "bias" ]] ;then
#    let ds="(abs($score1) - abs($score2)) / $conf1"
    let ds="abs($score1 - $score2) / $conf1"
    let sss="(abs($score1) - abs($score2))"
    if (( $sss <  0 )); then let ds="-$ds"; fi
  elif [[ $stat = "rms" ]] ;then
    let ds="($score1 - $score2) / $conf1"
  else
    let ds="($score2 - $score1) / $conf1"
  fi
  let ds95="$ds"
  let ds99="$ds * $alpha1 / $alpha2"
  let ds999="$ds * $alpha1 / $alpha3"
  ds=`printf "%7.3f" $ds`
  ds95=`printf "%7.3f" $ds95`
  ds99=`printf "%7.3f" $ds99`
  ds999=`printf "%7.3f" $ds999`
fi

if (( $ds999 >= 1 )); then
  sym=$(echo '<td><font color="#009120">&#9650;</font></td>')
  state=$(echo "$mdnamec2 is better than $mdnamec1 at the 99.9% significance level")
elif (( $ds999 < 1 && $ds99 >= 1 )); then
  sym=$(echo '<td><font color="#009120">&#9652;</font></td>')
  state=$(echo "$mdnamec2 is better than $mdnamec1 at the 99% significance level")
elif (( $ds99 < 1 && $ds95 >= 1 )); then
  sym=$(echo '<td style="background:#A9F5A9"></td>')
  state=$(echo "$mdnamec2 is better than $mdnamec1 at the 95% significance level")
elif (( $ds95 > -1 && $ds95 < 1 )); then
  sym=$(echo '<td style="background:#BDBDBD"></td>')
  state=$(echo "No statistically significant difference between $mdnamec2 and $mdnamec1")
elif (( $ds95 <= -1 && $ds99 > -1 )); then
  sym=$(echo '<td style="background: #F5A9BC"></td>')
  state=$(echo "$mdnamec2 is worse than $mdnamec1 at the 95% significance level")
elif (( $ds99 <= -1 && $ds999 > -1 )); then
  sym=$(echo '<td><font color="#FF0000">&#9662;</font></td>')
  state=$(echo "$mdnamec2 is worse than $mdnamec1 at the 99% significance level")
elif (( $ds999 <= -1 && $ds999 > -100.0 )); then
  sym=$(echo '<td><font color="#FF0000">&#9660;</font></td>')
  state=$(echo "$mdnamec2 is worse than $mdnamec1 at the 99.9% significance level")
elif (( $ds999 < -100.0 )); then
  sym=$(echo '<td>M</td>')
fi

if [ $ds = $undef ] ; then
  sym=$(echo '<td style="background:#58ACFA"></td>') 
fi

#For Anom Correlation Temperature in tropics, make table value blank
if [[ $stat = "cor" && $reg =~ "TRO" ]] ; then
  sym=$(echo '<td style="background:#58ACFA"></td>')
fi


cat <<EOFF >> $htfile
       $sym
EOFF

fi
done #End of day loop

done #End of region loop
cat <<EOF >> $htfile
   </tr>

   <tr>
EOF

done #End of level loop

done #End of vnam HGT WIND loop

done #End of stat cor bias rmse

cat <<EOF >> $htfile
    </tbody>
   </table>
EOF


#Create the legend.html file
cat <<legend >> $legfile
<link type="text/css" rel="stylesheet" href="scorecard.css"/>
<div>
    <table class="second" cellpadding="0.2">
    <tr>
       <th colspan=2>EMC Verification Scorecard</th>
    </tr>
    <tr>
       <th colspan=2>Symbol Legend</th>
    </tr>
    <tr class="legend">
      <td><font color="#009120">&#9650;</font></td>
      <td>$mdnamec2 is better than $mdnamec1 at the 99.9% significance level</td>
    </tr>
    <tr class="legend">
      <td><font color="#009120">&#9652;</font></td>
      <td>$mdnamec2 is better than $mdnamec1 at the 99% significance level</td>
    </tr>
    <tr class="legend">
      <td style="background:#A9F5A9"></td>
      <td>$mdnamec2 is better than $mdnamec1 at the 95% significance level</td>
    </tr>
    <tr class="legend">
      <td style="background:#BDBDBD"></td>
      <td>No statistically significant difference between $mdnamec2 and $mdnamec1</td>
    </tr>
    <tr class="legend">
      <td style="background: #F5A9BC"></td>
      <td>$mdnamec2 is worse than $mdnamec1 at the 95% significance level</td>
    </tr>
    <tr class="legend">
      <td><font color="#FF0000">&#9662;</font></td>
      <td>$mdnamec2 is worse than $mdnamec1 at the 99% significance level</td>
    </tr>
    <tr class="legend">
      <td><font color="#FF0000">&#9660;</font></td>
      <td>$mdnamec2 is worse than $mdnamec1 at the 99.9% significance level
    </tr>
    <tr class="legend">
      <td style="background:#58ACFA"</td>
      <td>Not statistically relevant</td>
    </tr>
    <tr>
      <th colspan=2>Start Date: $SDATE </th>
    </tr>
    <tr>
      <th colspan=2>End Date: $EDATE </th>
    </tr>
legend

#Create css file for border
cat << CSSEND >> $cssfile
body {
        margin : 0;
        padding : 0;
        background-color : #ffffff;
        color : #000000;
        }
.first {
        border-collapse: collapse;
        border: 3px solid black;
        }
.second {
        border-collapse: collapse;
	border: 1px dashed black;
}
.legend {
        font-size: 0.75em;
}
#bold {
        font: bold 1em Times;
	}

td {
        border-collapse: collapse;
        border: 2px solid black;
}
th {
        border-collapse: collapse;
        border: 1px solid black;
        color: red;
        font-family: Garamound;
}
#thside {
        color: blue;
        font-family: Garamound;
}
CSSEND

#Create main index file
cat << MAIN >> $mainfile
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>
    <title>EMC Verification Scorecard</title>
      <frameset cols="20%,80%">
        <frame src="$legfile">
	<frame src="$htfile">
        <link type="text/css" rel="stylesheet" href="$cssfile"/>
  </head>
      </frameset>
</html>
MAIN

if [ ! -s $mapdir/scorecard ]; then
  mkdir -p $mapdir/scorecard
fi

 cp *html $mapdir/scorecard/.
 cp  *css $mapdir/scorecard/.


echo $mapdir/scorecard

exit
