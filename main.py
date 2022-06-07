# google sheet api module/ pandas for preprocessing
import gspread
import pandas as pd
import tenant_info


# set appropriate timezones based on tenant dictionary
def set_timezones(tenant):
    timezone = ''
    if tenant in tenant_info.TENANT_TIMEZONES['pacific']:
        timezone = 'America/Los_Angeles'
    elif tenant in tenant_info.TENANT_TIMEZONES['mountain']:
        timezone = 'America/Denver'
    elif tenant in tenant_info.TENANT_TIMEZONES['central']:
        timezone = 'America/Chicago'
    elif tenant in tenant_info.TENANT_TIMEZONES['eastern']:
        timezone = 'America/New_York'
    return timezone


# setting cohort name based on timezone
def set_cohort(tenant):
    cohort = ''
    if tenant in tenant_info.TENANT_TIMEZONES['pacific']:
        cohort = '2022-05-24-fesd-pacific'
    elif tenant in tenant_info.TENANT_TIMEZONES['mountain']:
        cohort = '2022-05-24-fesd-mountain'
    elif tenant in tenant_info.TENANT_TIMEZONES['central']:
        cohort = '2022-05-24-fesd-central'
    elif tenant in tenant_info.TENANT_TIMEZONES['eastern']:
        cohort = '2022-05-24-fesd-eastern'
    return cohort


# use gspread to access correct workspace and sheet
sa = gspread.service_account()
sh = sa.open("2022 Roster")
wks = sh.worksheet("joestest")

# initial pandas preprocessing - converting gspread dataframe, reindexing columns, handle null values etc...
df = pd.DataFrame(wks.get_all_records())\
    .reindex(columns=['username', 'firstname', 'lastname', 'email', 'tenant', 'program1', 'timezone', 'profile_field_ptcohort', 'Notes'])\
    .replace("", float('NaN'))\
    .dropna(subset=['firstname'])\
    .reset_index(drop=True)

# dropping sheet outliers
df = df.drop(df[df.tenant == 'Total # of Students:'].index)

# 'Notes' column contains conditions on tentative or removed students - standardizing and dropping where necessary
df['Notes'] = df['Notes'].str.lower()
df = df.drop(df[df.Notes == 'wait'].index)
df = df.drop(df[df.Notes == 'drop'].index)
df = df.drop(df[df.Notes == 'pending'].index)\
    .reset_index(drop=True)

# column cleanup and functions applied
df['username'] = df['email']
df['program1'] = 'FESD202205'
df['timezone'] = df['tenant'].apply(set_timezones)
df['profile_field_ptcohort'] = df['tenant'].apply(set_cohort)

# final file
final_df = df.drop(columns=['Notes'])

# convert to csv. Ready for upload
final_df.to_csv('may_2022_uploads_test.csv', encoding='utf-8', index=False)




