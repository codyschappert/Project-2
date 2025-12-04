import logic

user_info = {'cschappert': {'password': '1234', 'checking': logic.Account('checking', 0), 'savings': logic.Account('savings', 0)}}
username = 'cschappert'
user_account = user_info[username]['checking']

accounts = user_info[username]
print(f"{accounts['checking'].get_balance():.2f}")

account_type ='checking'
print(accounts[account_type])
