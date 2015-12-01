import xlsxwriter as xlsx

country_name_ISO2_code = {"AU": "Austrilia", "CA": "Canada", "DE": "Germany", "ES": "Spain", "FR": "France", "GB": "United Kingdom", "IT": "Italy", "NL": "Netherlands", "PT": "Portugal", "US": "United States"}

def get_destination_country_name_list():
	workbook = xlsxwriter.Workbook('../data/destination_country_name.xlsx')
	worksheet = workbook.add_worksheet()
	row, col = 0, 0
	worksheet.write(row, col, "Country")
	worksheet.write(row, col + 1, "ISP2 Code")
	row += 1

get_destination_country_name_list()