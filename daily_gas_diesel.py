import aiohttp
from pyfuelprices import FuelPrices

class TellMeGasDieselPrice:
    def __init__(self):
        self.diesel_data = {}
        self.gas_data = {}

    async def call_data(self):
        async with aiohttp.ClientSession() as session:
            fp = FuelPrices.create(client_session=session, configuration={"providers": {"gasbuddy": {}}})
            stations = await fp.find_fuel_locations_from_point((49.8951, -97.1384), 10.0, source_id="gasbuddy")

        return stations
    
    def get_gas_price(self, stations):
        gas_data_dict = {}
        for station in stations[:5]:
            try:
                name = station['name'].split()[0]
                code = station['postal_code']
                gas_price = station.get("available_fuels")['regular_gas']
                if name in gas_data_dict:
                    exist_price = gas_data_dict[name]['regular_gas']
                    if gas_price < exist_price:
                        gas_data_dict[name]={
                            'postal_code': code,
                            'regular_gas': gas_price
                        }

                else:
                    gas_data_dict[name] = {
                        "postal_code": code,
                        "regular_gas": gas_price
                    }

            except Exception as e:
                continue

        return gas_data_dict

    def get_diesel_price(self, stations):
        diesel_data_dict = {}
        for station in stations[:5]:
            try:
                name = station['name'].split()[0]
                code = station['postal_code']
                diesel_price = station.get("available_fuels")['diesel']
                if diesel_price==0:
                    continue
                # print(f"{idx} {name} : {code} : ${diesel_price}")
                if name in diesel_data_dict:
                    exist_price = diesel_data_dict[name]['diesel_price']
                    if diesel_price < exist_price:
                        diesel_data_dict[name]={
                            'postal_code': code,
                            'diesel_price': diesel_price
                        }
                else:
                    diesel_data_dict[name] = {
                        "postal_code": code,
                        "diesel_price": diesel_price
                    }
            except Exception as e:
                continue
            
        return diesel_data_dict
    
    def sorted_price(self, price_info:dict, oil_type:str):
        """oil_type = regular_gas_price or diesel_price"""
        # 가격 기준 내림차순(가장 비싼 곳부터) 정렬
        sorted_data = dict(
            sorted(
                price_info.items(),
                key=lambda item: item[1][oil_type],
                reverse=False
            )
        )
        return sorted_data
    
    def get_string(self, gas_info_list:list, diesel_info_list:list):
        diesel_station_name = list(diesel_info_list.keys())[0]
        diesel_station_pcode = diesel_info_list[list(diesel_info_list.keys())[0]]['postal_code']
        diesel_station_price = diesel_info_list[list(diesel_info_list.keys())[0]]['diesel_price']

        gas_station_name = list(gas_info_list.keys())[0]
        gas_station_pcode = gas_info_list[list(gas_info_list.keys())[0]]['postal_code']
        gas_station_gas_price = gas_info_list[list(gas_info_list.keys())[0]]['regular_gas']

        diesel_text = f"{diesel_station_name}, {diesel_station_pcode} 지점의 디젤 가격 = ${diesel_station_price}"
        gasoline_text = f"{gas_station_name}, {gas_station_pcode} 지점의 가솔린 가격 = ${gas_station_gas_price}"

        return gasoline_text, diesel_text        