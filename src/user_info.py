from datetime import datetime
import pandas as pd
import json


column_names = ['user_id', 'appt', 'splan', 'end_date']
def get_next_billing_date(subscription_date):
    subcription_day = subscription_date.strftime('%d')
    billing_day = pd.Timestamp.now().strftime('%d')
    billind_month_year = pd.Timestamp.now().strftime('%Y-%m')
    if int(subcription_day)>int(billing_day):
        return pd.Timestamp(billind_month_year+'-'+subcription_day)
    else:
        print(billing_day+billind_month_year)
        return pd.Timestamp(billind_month_year+'-'+billing_day)

class UserInfo:

    def __init__(self):

        self.input_data = None

    def load_data(self, data):
        data = pd.read_csv(data,
                                  sep=',',
                                  parse_dates=['Appointment Date', 'Final Delivery Date/Subscription End Date'],
                                  keep_default_na=True,
                                  mangle_dupe_cols=True)
        data.columns = column_names
        data['is_active'] = data.apply(lambda x: '1' if x['end_date'] is pd.NaT else '0', axis=1)
        data = data.sort_values(['user_id', 'appt'])
        # dropping duplicates

        self.input_data = pd.DataFrame(columns=column_names)
        for index1, row in data.iterrows():
            index = self.input_data.index[self.input_data['user_id'] == row['user_id']]
            if len(index) == 1:
                self.input_data.at[index[0],'splan'] = row['splan']
                if self.input_data._get_value(index[0],'is_active') == '0':
                    self.input_data.at[index[0],'appt'] = row['appt']
                    self.input_data.at[index[0],'is_active'] = row['is_active']
            else:
                self.input_data = self.input_data.append(row)

    def get_user_info(self, user_id):
        index = self.input_data.index[self.input_data['user_id'] == user_id]
        if len(index) == 1:
            data= {"userId" :self.input_data._get_value(index[0],'user_id'),
                "currentPlan":self.input_data._get_value(index[0],'splan'),
                "subscriptionStartDate":self.input_data._get_value(index[0],'appt').strftime('%m %d, %Y'),
                "nextBillingDate": get_next_billing_date(self.input_data._get_value(index[0],'appt')).strftime('%m/%d/%Y'),
                "isActive" :"True" if self.input_data._get_value(index[0],'is_active') == '1' else "False"}
            return json.dumps(data)
        return None

    



