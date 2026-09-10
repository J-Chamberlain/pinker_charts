cd "C:\Users\jwolfers\Documents\Justin@Wharton\Happiness and growth\Data for Brookings"
clear
set more off
set mem 800m
set matsize 2000
set scheme s1color

* GDP: Merge together assorted GDP datasets to create our basic GDP data
do "GDP\Complete_GDP.do"

* World Values Survey 
* Raw WVS data are in a file called "xwvsevs_1981_2000_v20060423.dta"
* Individual country codes are in "WVS income coding.do", which are called by "WVS setup.do"
* Yields usable micro and macro files: WVS.dta and WVS_macro.dta
do "WVS\WVS setup.do"
cap log close
log using "WVS\WVS_results.log", text replace
do "WVS\WVS micro analysis.do"
do "WVS\WVS macro analysis.do"
do "WVS\WVS appendices.do"
 

* Eurobarometer:
cap log close
log using "Eurobarometer\Eurobarometer.log", text replace
do "Eurobarometer\Eurobarometer setup.do"
do "Eurobarometer\Eurobarometer analysis.do"
log close

* Pew Survey
cap log close
log using "Pew\Pew.log", text replace
do "Pew\Pew setup.do"
do "Pew\Pew analysis.do"
log close

* General Social Survey
cap log close
log using "GSS\GSS.log", text replace
do "GSS\GSS setup.do"
do "GSS\GSS analysis.do"
log close

* Japan Life-in-Nation
cap log close
log using "Japan\Japan.log", text replace
do "Japan\Japan analysis.do"
log close

* Historical
cap log close
log using "History\History.log", text replace
do "History\Fig1.do"
do "Other surveys\Happiness v Life Sat.do"
log close
