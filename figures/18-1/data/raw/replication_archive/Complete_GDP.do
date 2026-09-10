clear

use "GDP\WDI GDP per capita"
sort cty year
merge cty year using "GDP\PWT"
tab cty _merge
drop if year<1960
gsort cty -year
by cty: replace gdp=gdp[_n-1]*cgdp/cgdp[_n-1] if gdp==.
levelsof year, local(years)
foreach y of local years {
	summ gdp if cty=="USA" & year==`y'
	local us_gdp=r(mean)
	summ cgdp if cty=="USA" & year==`y'
	local us_cgdp=r(mean)
	replace gdp=cgdp*`us_gdp'/`us_cgdp' if gdp==. & year==`y'
}

rename _merge _merge_pwt
sort cty year
merge cty year using "GDP\BLS GDP per capita"
drop if year<1960
gen usa_gdp=gdp if cty=="USA"
tomode usa_gdp, by(year) replace
replace gdp=blsgdp*usa_gdp/usa_blsgdp if gdp==. & cty=="FRG" /* Create an appropriately-scaled series for FRG */
rename _merge _merge_bls
sort cty year
merge cty year using "GDP\Germany"
rename _merge _merge_germany
sort cty year
by cty: replace gdp=gdp[_n-1]*german_gdp/german_gdp[_n-1] if gdp==. & cty=="FRG" /* Forward-cast the FRG series */
gen germany_frg=german_gdp if cty=="FRG"
gen germany_gdr=german_gdp if cty=="GDR"
gen gdp_frg=gdp if cty=="FRG"
for X in varlist germany_frg germany_gdr gdp_frg: tomode X, by(year) replace
replace gdp=gdp_frg*germany_gdr/germany_frg if cty=="GDR"

* Also merge in world factbook
summ gdp if cty=="USA" & year==2004
local ratio2004=r(mean)/40100
replace gdp=`ratio2004'*3500 if cty=="IRQ" & year==2004 /* 2005 World factbook */
summ gdp if cty=="USA" & year==2006
local ratio2006=r(mean)/43500
summ year
local o=r(N)+1
set obs `o'
replace cty="UNK" if cty==""
replace year=2006 if cty=="UNK"
replace countryname="Kosovo" if cty=="UNK"
for X in any MMR BIH CUB IRQ KWT MNE PRI SRB ARE UNK SAU \ Y in num 1800 5500 3900 2900 21600 3800 19100 7200 49700 1800 13800: replace gdp=Y*`ratio2006' if cty=="X" & year==2006 /* 2007 World factbook */

sort cty year
saveold "Processed files\Complete_GDP", replace
