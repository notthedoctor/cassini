# Cassini

## Image database

The Cassini data files are accessible through an API at root directory https://pds-imaging.jpl.nasa.gov/w10n/cassini/cassini_orbiter. The Imaging Sub System (ISS) is contained in a set of directories within this that correspond to periods of time. Within these directories are sub-directories that further partition the images by time and within that are the data files. There isn't much information to be found from the data file name but each data file does have a text summary associated with it. There are version directories and the like so my final list of the first set of ISS directories is below:

```
'coiss_0001', 'coiss_0002', 'coiss_0003', 'coiss_0004', 'coiss_0005',
 'coiss_0006', 'coiss_0007', 'coiss_0008', 'coiss_0009', 'coiss_0010',
 'coiss_0011_v4.3', 'coiss_1001', 'coiss_1002', 'coiss_1003', 'coiss_1004',
 'coiss_1005', 'coiss_1006', 'coiss_1007', 'coiss_1008', 'coiss_1009',
 'coiss_2001', 'coiss_2002', 'coiss_2003', 'coiss_2004', 'coiss_2005',
 'coiss_2006', 'coiss_2007', 'coiss_2008', 'coiss_2009', 'coiss_2010',
 'coiss_2011', 'coiss_2012', 'coiss_2013', 'coiss_2014', 'coiss_2015',
 'coiss_2016', 'coiss_2017', 'coiss_2018', 'coiss_2019', 'coiss_2020',
 'coiss_2021', 'coiss_2022', 'coiss_2023', 'coiss_2024', 'coiss_2025',
 'coiss_2026', 'coiss_2027', 'coiss_2028', 'coiss_2029', 'coiss_2030',
 'coiss_2031', 'coiss_2032', 'coiss_2033', 'coiss_2034', 'coiss_2035',
 'coiss_2036', 'coiss_2037', 'coiss_2038', 'coiss_2039', 'coiss_2040',
 'coiss_2041', 'coiss_2042', 'coiss_2043', 'coiss_2044', 'coiss_2045',
 'coiss_2046', 'coiss_2047', 'coiss_2048', 'coiss_2049', 'coiss_2050',
 'coiss_2051', 'coiss_2052', 'coiss_2053', 'coiss_2054', 'coiss_2055',
 'coiss_2056', 'coiss_2057', 'coiss_2058', 'coiss_2059', 'coiss_2060',
 'coiss_2061', 'coiss_2062', 'coiss_2063', 'coiss_2064', 'coiss_2065',
 'coiss_2066', 'coiss_2067', 'coiss_2068', 'coiss_2069', 'coiss_2070',
 'coiss_2071', 'coiss_2072', 'coiss_2073', 'coiss_2074', 'coiss_2075',
 'coiss_2076', 'coiss_2077', 'coiss_2078', 'coiss_2079', 'coiss_2080',
 'coiss_2081', 'coiss_2082', 'coiss_2083', 'coiss_2084', 'coiss_2085',
 'coiss_2086', 'coiss_2087', 'coiss_2088', 'coiss_2089', 'coiss_2090',
 'coiss_2091', 'coiss_2092', 'coiss_2093', 'coiss_2094', 'coiss_2095',
 'coiss_2096', 'coiss_2097', 'coiss_2098', 'coiss_2099', 'coiss_2100',
 'coiss_2101', 'coiss_2102', 'coiss_2103', 'coiss_2104', 'coiss_2105',
 'coiss_2106', 'coiss_2107', 'coiss_2108', 'coiss_2109', 'coiss_2110',
 'coiss_2111', 'coiss_2112', 'coiss_2113', 'coiss_2114', 'coiss_2115',
 'coiss_2116', 'coiss_3001', 'coiss_3002_v3', 'coiss_3003_v1', 'coiss_3004',
 'coiss_3005_v1', 'coiss_3006_v4', 'coiss_3007'
```

Our first job is going to be constructing a database of these images, there are something like 300k of these images and the current recommended method is to use *wget* to pull the entire data set. It takes about a second just in turnaround time for the labels so just pulling the labels will take a few days and a couple of Gb. We will probably want to select interesting images based on the label and minimize the amount we have to download from this very slow server. So we can improve our label stripping code we just pull a local copy of the labels using the file *src/pull_label_files.py*.