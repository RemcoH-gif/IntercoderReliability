import pandas as pd
from Code import InterRater_Reliability as IRR

path = str(r'C:\Users\remco\PycharmProjects\IRR\Data')

df_remco = pd.read_excel(path+r'\codering Remco.xlsx')
df_remco = IRR.remove_letter(df_remco)
df_cc_remco, serie_cc_remco = IRR.category_count(df_remco)

df_bjorn = pd.read_excel(path+r'\codering Björn.xlsx')
df_bjorn = IRR.remove_letter(df_bjorn)
df_cc_bjorn, serie_cc_bjorn = IRR.category_count(df_bjorn)

df_saskia = pd.read_excel(path+r'\codering Saskia.xlsx')
df_saskia = IRR.remove_letter(df_saskia)
df_cc_saskia, serie_cc_saskia= IRR.category_count(df_saskia)

df_maaike = pd.read_excel(path+r'\codering Maaike.xlsx')
df_maaike = IRR.remove_letter(df_maaike)
df_cc_maaike, serie_cc_maaike = IRR.category_count(df_maaike)

cc_series = [serie_cc_remco, serie_cc_bjorn, serie_cc_maaike, serie_cc_saskia]
names = ['Remco', 'Björn', 'Maaike', 'Saskia']

cc_combined, serie_classifier = IRR.combine_series(cc_series, names)

df_key_stat = pd.DataFrame(index=serie_classifier)
cc_combined, df_key_stat = IRR.add_bland_altman_stat(cc_combined, df_key_stat)

df_key_stat = IRR.pearson_corr(cc_combined, df_key_stat)

print(df_key_stat)




