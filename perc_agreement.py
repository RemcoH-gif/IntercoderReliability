import pandas as pd
from Code import InterRater_Reliability as IRR

path = str(r'C:\Users\remco\PycharmProjects\IRR\Data')

df_remco = pd.read_excel(path+r'\codering Remco.xlsx')
df_remco = IRR.remove_letter(df_remco)
df_remco = IRR.uniformize_length(df_remco, 350)

df_bjorn = pd.read_excel(path+r'\codering Björn.xlsx')
df_bjorn = IRR.remove_letter(df_bjorn)
df_bjorn = IRR.uniformize_length(df_bjorn, 350)

df_maaike = pd.read_excel(path+r'\codering Maaike.xlsx')
df_maaike = IRR.remove_letter(df_maaike)
df_maaike = IRR.uniformize_length(df_maaike, 350)

df_saskia = pd.read_excel(path+r'\codering Saskia.xlsx')
df_saskia = IRR.remove_letter(df_saskia)
df_saskia = IRR.uniformize_length(df_saskia, 350)

category_series = [df_remco, df_bjorn, df_maaike, df_saskia]
names = ['Remco', 'Björn', 'Maaike', 'Saskia']

df_perc = IRR.stack_series(category_series, names)

df_perc, perc_agreement = IRR.perc_agreement(df_perc)

print(perc_agreement)
