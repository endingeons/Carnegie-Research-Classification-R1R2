# ETL Tools
This folder contains Python tools to perform the Extract-Tranform-Load workflow to get our original CSVs into a usable format in our MySQL database for further analysis

# Data Selection

The objective of HW 6 and 7 is to advise Rowan University on the most important factors that will improve Rowan's stance as a R2 Research University to R1 Research University. Machine learning will be utilized to classify R1/R2 universities and see the dominant contributing factors to the classification. To achieve this the data selected come directly from the Carnegie Classification of Institutions of Higher Education (CCIHE) and the National Science Foundation (NSF).

Four data tables are used. The first two are the qualitative characteristics of the R1/R2 universities as described by the CCIHE. Not all fields will be used in the classifier but all fields are preserved for data exploration purposes. Additionally, the data that was used to build the CCIHE statistical model to classify R1/R2 universities was incorporated from the CCIHE website. The link to the the CCIHE research methods of the Carnegie Classifications and the data sources are linked in the Appendix. Finally, NSF ranking data describing the percentile of full time graduate students and amount of research space was incorporated to round out the data.

Data for a total of 274 universities was combined into a MySQL database. Detailed descriptions of the data and an EER Diagram of the MySQL database are available in the Appendix section.

# Data Cleaning and Modification

Several steps were taken to clean up the data so all four tables could be combined and unified based on the unique University ID provided by CCIHE.

1. The research methods of the CCIHE classification indicate the exclusion of Rutgers University Camden, Thomas Jefferson University, and Marshall University which are missing data for certain necessary fields used in the original Carnegie Classification
2. Exclude all CCIHE data that is not related to an R1 or R2 university, based on the BASIC2021 field that indicates the 2021 Carnegie Classification of the university (want to keep enum 15, 16 which are high and very high doctoral research activity)

Data sets were relatively clean, no missing data. However to join the tables together many steps had to be taken to modify the names of the universities so they could be matched together and unioned between the NSF data set and the Carnegie datasets. Cleaning the names of the universities made it so 258 of 274 names could be successfully matched programmatically. The 16 remaining names had to be manually mapped between datasets. For the future, an AI approach could've been used to map university names between databases instead of programming the following corrections:

1. Change abbreviated 'C.' and 'U.' to College and University
2. Remove commas in names
3. Removed all stopwords like 'the, 'of', 'in', 'at'
4. Remove dashes in name
5. Handle A & M or A & T to A&M and A&T
6. Remove Main Campus or Campus from the NSF data, as this was not indicated in the CCIHE data
7. Replace St with Saint
8. Remove SUNY from names (no indication of SUNY in Carnegie data, only in NSF)
9. Additional cleanup to remove trailing, leading, or duplicate spaces

Two university names were excluded as they had no apparent match between Carnegie and NSF data sets. 'Arizona State University Campus Immersion' and 'Arizona State University Digital Immersion'

# Appendix

Link to GitHub Repository: [https://github.com/endingeons/Carnegie-Research-Classification-R1R2](https://github.com/endingeons/Carnegie-Research-Classification-R1R2)

**Table 1: Data Table Sources**

| **Table Name** | **Source** | **Description** |
| --- | --- | --- |
| **cc\_download\_R1.csv** | [https://carnegieclassifications.acenet.edu/institutions/?basic2021\_\_du%5B%5D=15](https://carnegieclassifications.acenet.edu/institutions/?basic2021__du%5B%5D=15) | Qualitative data to characterize the R1 universities. |
| **cc\_download\_R2.csv** | [https://carnegieclassifications.acenet.edu/institutions/?basic2021\_\_du%5B%5D=16](https://carnegieclassifications.acenet.edu/institutions/?basic2021__du%5B%5D=16) | Qualitative data to characterize the R2 universities. |
| **CCIHE2021-PublicData.xlsx** | [https://carnegieclassifications.acenet.edu/wp-content/uploads/2023/03/CCIHE2021-PublicData.xlsx](https://carnegieclassifications.acenet.edu/wp-content/uploads/2023/03/CCIHE2021-PublicData.xlsx) | The Carnegie Classification of Institutions of Higher Education - Research Activity Index - Methodology Details. Data set used by Carnegie Classification as described in their research methods: [https://carnegieclassifications.acenet.edu/wp-content/uploads/2023/04/CCIHE2021\_Research\_Activity\_Index\_Method.pdf](https://carnegieclassifications.acenet.edu/wp-content/uploads/2023/04/CCIHE2021_Research_Activity_Index_Method.pdf) |
| **rankings.xlsx** | [https://ncsesdata.nsf.gov/profiles/site?method=ranking](https://ncsesdata.nsf.gov/profiles/site?method=ranking) | NSF quantitative ranking data for all universities |

**Table 2: Description of Variables**

| **Variable Name** | **Source Table** | **Description** |
| --- | --- | --- |
| University Key | cc\_download\_R1.csv/ cc\_download\_R2.csv | Unique identifier for the university |
| Name | cc\_download\_R1.csv/ cc\_download\_R2.csv | University name |
| City | cc\_download\_R1.csv/ cc\_download\_R2.csv | City |
| State | cc\_download\_R1.csv/ cc\_download\_R2.csv | State |
| Level | cc\_download\_R1.csv/ cc\_download\_R2.csv | Degrees (four or more years) |
| Control | cc\_download\_R1.csv/ cc\_download\_R2.csv | Public or private non-profit |
| Undergraduate Program | cc\_download\_R1.csv/ cc\_download\_R2.csv | Undergraduate program Carnegie Classification (e.g. 'Arts & sciences plus professions some graduate coexistence') |
| Graduate Program | cc\_download\_R1.csv/ cc\_download\_R2.csv | Research with or without a medical/veterinary school |
| Enrollment Profile | cc\_download\_R1.csv/ cc\_download\_R2.csv | Enrollment composition majority undergrads or grad students |
| Undergraduate Profile | cc\_download\_R1.csv/ cc\_download\_R2.csv | Graduate composition, four-year degrees with high to low transfer |
| Size Setting | cc\_download\_R1.csv/ cc\_download\_R2.csv | Size and residential or nonresidential setting |
| Basic | cc\_download\_R1.csv/ cc\_download\_R2.csv | R1 or R2 classification (high or very high research activity) |
| Community Engagement | cc\_download\_R1.csv/ cc\_download\_R2.csv | Community engagement classified or not classified |
| SERD | CCIHE2021-PublicData.xlsx | Science & Engineering Research & Development Expenditures ($Thousands) |
| NONSERD | CCIHE2021-PublicData.xlsx | Non Science & Engineering Research & Development Expenditures ($Thousands) |
| PDNFRSTAFF | CCIHE2021-PublicData.xlsx | Postdoctorates and non-faculty research staff with doctorates |
| FACNUM | CCIHE2021-PublicData.xlsx | Number full-time of faculty in ladder rank (assistant, associate, and full professors) Fall 2020 |
| HUM\_RSD | CCIHE2021-PublicData.xlsx | Humanities research/scholarship doctoral degrees |
| STEM\_RSD | CCIHE2021-PublicData.xlsx | Social Science research/scholarship doctoral degrees |
| OTH\_RSD | CCIHE2021-PublicData.xlsx | Number of research/scholarship doctoral degrees conferred in professional fields |
| Percentile Full Time Graduate | rankings.xlsx | Historical rankings based on total number of full time graduate students |
| Percentile Research Space | rankings.xlsx | Historical rankings based on the total net assignable square feet in Science and engineering research space in academic institutions |

![](RackMultipart20230813-1-ctuamq_html_882664dd91f1a929.png)

**Figure 1: EER Diagram of Research University Database**

