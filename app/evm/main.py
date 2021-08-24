from .farms import farms
from . import external_contracts
from . import farm_templates

def return_farms_list():
    return farms

async def get_evm_positions(wallet,farm_id):
    farm_configuraiton = farms[farm_id]
    farm_network = farm_configuraiton['network']
    masterchef_pool_list = [farm_id]
    args = {'wallet' : wallet}
    returned_object = ({},{farm_id : {'name' : farm_configuraiton['name'], 'network' : farm_configuraiton['network'], 'wallet' : wallet, 'userData' : {}}})

    if farm_configuraiton['stakedFunction'] is not None:
        masterchef = await farm_templates.get_traditional_masterchef(wallet, masterchef_pool_list, farm_network, farm_configuraiton, returned_object[1])
        if masterchef is not None:
            returned_object[0].update(masterchef[0])
            returned_object[1][farm_id]['userData'].update(masterchef[1][farm_id]['userData'])
    if 'extraFunctions' in farm_configuraiton:

        if farm_configuraiton['extraFunctions']['vaults'] is not None:
            vaults = []
            for vf in farm_configuraiton['extraFunctions']['vaults']:
                vault = await vf()
                vaults.append(vault)
        
        if farm_configuraiton['extraFunctions']['args'] is not None:
            args.update(farm_configuraiton['extraFunctions']['args'])

        for i,f in enumerate(farm_configuraiton['extraFunctions']['functions']):
            farm_info = await f(vaults=vaults[i], **args)
            
            if farm_info is not None:
                returned_object[0].update(farm_info[0])
                returned_object[1][farm_id]['userData'].update(farm_info[1][farm_id]['userData'])
        

    return returned_object[1]
                

    # x = await external_contracts.get_beefy_bsc()
    # print(x)




