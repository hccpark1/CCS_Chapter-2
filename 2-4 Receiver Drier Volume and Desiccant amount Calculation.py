### AC Receiver Drier Volume and Desiccant amount Calculation.py


def calculate_moisture_system(system_volume_cc, rho_air_g_per_L, abs_humidity_mg_per_g_air) :  # V1: 공기 중 수분량 (Ms)
    system_volume_L = system_volume_cc / 1000
    Ms = abs_humidity_mg_per_g_air * rho_air_g_per_L * system_volume_L   # mg
    Ms = Ms * 0.1                   # 전체 시스템 체적 중에서 냉매 추진 후 10% 체적 상당 공기에만 수분 함유 가정
    return Ms

def calculate_moisture_refrigerant(ref_mass_g) :    # V2: 냉매 수분량 (Mr)
    ref_liquid_mg_per_kg=10     # R134a 액상 냉매 1kg당 수분량 (mg/kg) @ 25C
    ref_quality=0.296            # R134a 건도 (0~1)
    Mr = (ref_liquid_mg_per_kg * (1 - ref_quality))/1000 * ref_mass_g   # mg
    return Mr


def calculate_moisture_oil(oil_mass_g) :    # V3: 오일 함유 수분량 (Mo)
    oil_mg_per_kg=100              # PAG 오일 수분 함유량 (mg/kg) @ 25C
    Mo = oil_mg_per_kg / 1000 * oil_mass_g   # mg
    return Mo

def calculate_hose_permeation() :                # V4 : 호스 침투 수분량 (Mp)
    s_factor = 1.0
    s_period = 5 # 사용기간 (년)
    
    hose_mg_per_m2_year = 50              # 호스 허용 침투 수분량 (mg/m2/year) 
    hose_area_m2 = 1000/10000                 # 실제 호스 표면적 예 (m2) 900 cm2
    Mp = hose_mg_per_m2_year * hose_area_m2 * s_factor * s_period   # 호스 침투 수분량 (mg/year) 
    return Mp
   
   
def calculate_system_moisture_remove(Ms, Mr, Mo, Mp) :       # V5: 전체 수분량 (Mt)
    Mt = Ms + Mr + Mo + Mp
    return Mt

def calculate_desiccant_mass(Mt) :              # V6: 흡습제 중량 계산 (XH-9 기준, 17.5% 흡착율)
    desiccant_absorption_rate = 0.175            # XH-9 흡착율  (17.5%) 
    SF =  1.25                                  # 안전율  (1.25)    
    desiccant_mass_g = (Mt / 10) / desiccant_absorption_rate * SF   # g
    return desiccant_mass_g

def calculate_drier_volume(refrigerant_charge_g, desiccant_g):
    """ 수액기 체적 계산 함수
    :param refrigerant_charge_g: 충진 냉매량 (g)
    :param desiccant_g: 흡습제 중량 (g)
    :return: 수액기 체적 (cc)   """
    refrigerant_storage_g = refrigerant_charge_g * 0.25         # V1 : 냉매 저장량 (충진량의 25%)
    fill_tolerance_g = 25                                       # V2 : 충진 여유량 (고정 25g) 
    desiccant_volume_cc = desiccant_g * 0.9     # V3 : 흡습제 중량 (입력값 사용),참고로 1g당 약 0.9cc로 환산
    residual_oil_g = refrigerant_charge_g * 0.03          # V4 : 수액기 내 잔유 오일량 (충진량의 3%)
    # 전체 중량 합산
    total_mass_g = refrigerant_storage_g + fill_tolerance_g + desiccant_g + residual_oil_g
    # 체적 환산 (0.9 곱함)
    drier_volume_cc = total_mass_g * 0.9 

    return drier_volume_cc

# 예시 실행
ref_mass_g = 600        # 충진 냉매량 (g)
oil_mass_g = 150        # 오일 중량 (g)
system_volume_cc=3200      # 시스템 내부 체적 (3100~3200 cc)
abs_humidity_mg_per_g_air=32.2  # 공기 중 절대 습도 (mg/g)
rho_air_g_per_L=1.085

Ms = calculate_moisture_system(system_volume_cc, rho_air_g_per_L, abs_humidity_mg_per_g_air)
Mr = calculate_moisture_refrigerant(ref_mass_g)
Mo = calculate_moisture_oil(oil_mass_g)
Mp = calculate_hose_permeation()
Mt = calculate_system_moisture_remove(Ms, Mr, Mo, Mp) 
desiccant_mass_g = calculate_desiccant_mass(Mt) 

# 결과 출력
print(f"충진 냉매량: {ref_mass_g} g")
print(f"오일량: {oil_mass_g} g")
print(f"공기 중 수분량 (Ms): {Ms:.1f} mg")
print(f"냉매 수분량 (Mr): {Mr:.1f} mg")
print(f"오일 수분량 (Mo): {Mo:.1f} mg")
print(f"호스 침투 수분량 (Mp): {Mp:.1f} mg")
print(f"전체 수분량 (Mt): {Mt:.1f} mg")
print(f"필요한 흡습제 중량 (XH-9 기준): {desiccant_mass_g:.1f} g")

drier_volume_cc = calculate_drier_volume(ref_mass_g, desiccant_mass_g)
# 결과 출력
print(f"수액기 예상 체적: {drier_volume_cc:.1f}cc")
print("\n")


