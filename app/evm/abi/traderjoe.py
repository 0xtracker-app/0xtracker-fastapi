abi = [{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"address","name":"_joe","internalType":"contract JoeToken"},{"type":"address","name":"_devAddr","internalType":"address"},{"type":"address","name":"_treasuryAddr","internalType":"address"},{"type":"address","name":"_investorAddr","internalType":"address"},{"type":"uint256","name":"_joePerSec","internalType":"uint256"},{"type":"uint256","name":"_startTimestamp","internalType":"uint256"},{"type":"uint256","name":"_devPercent","internalType":"uint256"},{"type":"uint256","name":"_treasuryPercent","internalType":"uint256"},{"type":"uint256","name":"_investorPercent","internalType":"uint256"}]},{"type":"event","name":"Add","inputs":[{"type":"uint256","name":"pid","internalType":"uint256","indexed":True},{"type":"uint256","name":"allocPoint","internalType":"uint256","indexed":False},{"type":"address","name":"lpToken","internalType":"contract IERC20","indexed":True},{"type":"address","name":"rewarder","internalType":"contract IRewarder","indexed":True}],"anonymous":False},{"type":"event","name":"Deposit","inputs":[{"type":"address","name":"user","internalType":"address","indexed":True},{"type":"uint256","name":"pid","internalType":"uint256","indexed":True},{"type":"uint256","name":"amount","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"EmergencyWithdraw","inputs":[{"type":"address","name":"user","internalType":"address","indexed":True},{"type":"uint256","name":"pid","internalType":"uint256","indexed":True},{"type":"uint256","name":"amount","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Harvest","inputs":[{"type":"address","name":"user","internalType":"address","indexed":True},{"type":"uint256","name":"pid","internalType":"uint256","indexed":True},{"type":"uint256","name":"amount","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"OwnershipTransferred","inputs":[{"type":"address","name":"previousOwner","internalType":"address","indexed":True},{"type":"address","name":"newOwner","internalType":"address","indexed":True}],"anonymous":False},{"type":"event","name":"Set","inputs":[{"type":"uint256","name":"pid","internalType":"uint256","indexed":True},{"type":"uint256","name":"allocPoint","internalType":"uint256","indexed":False},{"type":"address","name":"rewarder","internalType":"contract IRewarder","indexed":True},{"type":"bool","name":"overwrite","internalType":"bool","indexed":False}],"anonymous":False},{"type":"event","name":"SetDevAddress","inputs":[{"type":"address","name":"oldAddress","internalType":"address","indexed":True},{"type":"address","name":"newAddress","internalType":"address","indexed":True}],"anonymous":False},{"type":"event","name":"UpdateEmissionRate","inputs":[{"type":"address","name":"user","internalType":"address","indexed":True},{"type":"uint256","name":"_joePerSec","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"UpdatePool","inputs":[{"type":"uint256","name":"pid","internalType":"uint256","indexed":True},{"type":"uint256","name":"lastRewardTimestamp","internalType":"uint256","indexed":False},{"type":"uint256","name":"lpSupply","internalType":"uint256","indexed":False},{"type":"uint256","name":"accJoePerShare","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"event","name":"Withdraw","inputs":[{"type":"address","name":"user","internalType":"address","indexed":True},{"type":"uint256","name":"pid","internalType":"uint256","indexed":True},{"type":"uint256","name":"amount","internalType":"uint256","indexed":False}],"anonymous":False},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"add","inputs":[{"type":"uint256","name":"_allocPoint","internalType":"uint256"},{"type":"address","name":"_lpToken","internalType":"contract IERC20"},{"type":"address","name":"_rewarder","internalType":"contract IRewarder"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"deposit","inputs":[{"type":"uint256","name":"_pid","internalType":"uint256"},{"type":"uint256","name":"_amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"dev","inputs":[{"type":"address","name":"_devAddr","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"devAddr","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"devPercent","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"emergencyWithdraw","inputs":[{"type":"uint256","name":"_pid","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"investorAddr","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"investorPercent","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract JoeToken"}],"name":"joe","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"joePerSec","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"massUpdatePools","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"owner","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"pendingJoe","internalType":"uint256"},{"type":"address","name":"bonusTokenAddress","internalType":"address"},{"type":"string","name":"bonusTokenSymbol","internalType":"string"},{"type":"uint256","name":"pendingBonusToken","internalType":"uint256"}],"name":"pendingTokens","inputs":[{"type":"uint256","name":"_pid","internalType":"uint256"},{"type":"address","name":"_user","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"lpToken","internalType":"contract IERC20"},{"type":"uint256","name":"allocPoint","internalType":"uint256"},{"type":"uint256","name":"lastRewardTimestamp","internalType":"uint256"},{"type":"uint256","name":"accJoePerShare","internalType":"uint256"},{"type":"address","name":"rewarder","internalType":"contract IRewarder"}],"name":"poolInfo","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"poolLength","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"renounceOwnership","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"bonusTokenAddress","internalType":"address"},{"type":"string","name":"bonusTokenSymbol","internalType":"string"}],"name":"rewarderBonusTokenInfo","inputs":[{"type":"uint256","name":"_pid","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"set","inputs":[{"type":"uint256","name":"_pid","internalType":"uint256"},{"type":"uint256","name":"_allocPoint","internalType":"uint256"},{"type":"address","name":"_rewarder","internalType":"contract IRewarder"},{"type":"bool","name":"overwrite","internalType":"bool"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setDevPercent","inputs":[{"type":"uint256","name":"_newDevPercent","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setInvestorAddr","inputs":[{"type":"address","name":"_investorAddr","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setInvestorPercent","inputs":[{"type":"uint256","name":"_newInvestorPercent","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setTreasuryAddr","inputs":[{"type":"address","name":"_treasuryAddr","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setTreasuryPercent","inputs":[{"type":"uint256","name":"_newTreasuryPercent","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"startTimestamp","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalAllocPoint","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferOwnership","inputs":[{"type":"address","name":"newOwner","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"treasuryAddr","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"treasuryPercent","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"updateEmissionRate","inputs":[{"type":"uint256","name":"_joePerSec","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"updatePool","inputs":[{"type":"uint256","name":"_pid","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"uint256","name":"rewardDebt","internalType":"uint256"}],"name":"userInfo","inputs":[{"type":"uint256","name":"","internalType":"uint256"},{"type":"address","name":"","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"withdraw","inputs":[{"type":"uint256","name":"_pid","internalType":"uint256"},{"type":"uint256","name":"_amount","internalType":"uint256"}]}]