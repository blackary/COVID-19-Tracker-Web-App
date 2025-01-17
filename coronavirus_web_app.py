import json
import time
import requests
import threading
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import folium

key = st.secrets["key"]
p_token = st.secrets["p_token"]

st.title("COVID-19 Tracker")
st.subheader(
    "This application shows all current COVID-19 case numbers, deaths, and recoveries on a worldwide and country-by-country basis")
st.caption("Created by Daniyal Dawood")


class Tracker:
    def __init__(self, key, p_token):
        self.key = key
        self.p_token = p_token
        self.params = {
            "key": self.key
        }
        self.stats = self.data()
    
    def data(self):
        case = requests.get(f"https://www.parsehub.com/api/v2/projects/{p_token}/last_ready_run/data",
                            params={"api_key": key})  # Use web scraping to find data
        stats = json.loads(case.text)  # Use the JSON format of the data
        return stats
    
    def worldwide_cases(self):
        world = self.stats["world_total"]  # Find total worldwide cases
        for data in world:
            if data["name"] == "Coronavirus Cases:":
                return data["world_cases"]
    
    def worldwide_deaths(self):
        world = self.stats["world_total"]  # Find total worldwide deaths
        for data in world:
            if data["name"] == "Deaths:":
                return data["world_cases"]
            
    def worldwide_recovered(self):
        world = self.stats["world_total"]  # Find total worldwide recoveries
        for data in world:
            if data["name"] == "Recovered:":
                return data["world_cases"]
            
    def state_info(self):
        country = self.stats["states"]
        return country

    def state_list(self):
        country = self.stats["states"]
        list_of_countries = []
        for data in country:
            list_of_countries.append(data["name"])
        list_of_countries.sort()
        return list_of_countries

    def show_state_info(self):
        country = self.stats["states"]  # Find info for a specific country
        state = country_selection
        for data in country:
            if data["name"].lower() == state.lower():
                return (
                    f"""Info for {state}
Cases: {data['states_cases']}
Deaths: {data['states_deaths']} 
Recoveries: {data['states_recovered']}""")

    def new_info(self):
        hello = requests.post(f'https://www.parsehub.com/api/v2/projects/{p_token}/run', params={"api_key": key})
        stats = json.loads(hello.text)

        def update():
            time.sleep(0.1)
            old_info = self.stats
            while True:
                new_info = stats
                if new_info != old_info:
                    self.stats = new_info
                    break
                time.sleep(5)

        thread = threading.Thread(target=update)
        thread.start()


data = Tracker(key, p_token)
data.new_info()

list_of_geo_info = [(33.7680065, 66.2385139), (41.000028, 19.9999619), (28.0000272, 2.9999825), (42.5407167, 1.5732033),
                    (-11.8775768, 17.5691241), (18.1954947, -63.0750234), (17.2234721, -61.9554608),
                    (-34.9964963, -64.9672817), (40.7696272, 44.6736646), (12.51756625, -69.98186415210564),
                    (-24.7761086, 134.755), (47.59397, 14.12456), (40.3936294, 47.7872508), (24.7736546, -78.0000547),
                    (26.1551249, 50.5344606), (24.4769288, 90.2934413), (13.1500331, -59.5250305),
                    (53.4250605, 27.6971358), (50.6402809, 4.6667145), (16.8259793, -88.7600927),
                    (9.5293472, 2.2584408), (32.30382, -64.7561647), (27.549511, 90.5119273),
                    (-17.0568696, -64.9912286), (44.3053476, 17.5961467), (-23.1681782, 24.5928742),
                    (-10.3333333, -53.2), (18.4024395, -64.5661642), (4.4137155, 114.5653908), (42.6073975, 25.4856617),
                    (12.0753083, -1.6880314), (-3.4264997, 29.932395), (7.0323598, 19.9981227),
                    (16.0000552, -24.0083947), (13.5066394, 104.869423), (4.6125522, 13.1535811),
                    (61.0666922, -107.991707), (17.56187, -63.138004249640304), (19.703182249999998, -79.9174627243246),
                    (15.6134137, 19.0156172), (33.96579515, -120.09189711105296), (-31.7613365, -71.3187697),
                    (35.000074, 104.999927), (4.099917, -72.9088133), (-12.2045176, 44.2832964),
                    (-2.9814344, 23.8222636), (-19.919672900000002, -157.9753368892878), (10.2735633, -84.0739102),
                    (45.5643442, 17.0118954), (23.0131338, -80.8328748), (12.21339425, -69.0408499890865),
                    (34.9823018, 33.1451285), (49.8167003, 15.4749544), (5.178633850000001, 97.14288663046936),
                    (-2.9814344, 23.8222636), (55.670249, 10.3333283), (11.8145966, 42.8453061),
                    (19.0974031, -70.3028026), (19.0974031, -70.3028026), (-1.3397668, -79.3666965),
                    (26.2540493, 29.2675469), (13.8000382, -88.9140683), (1.613172, 10.5170357),
                    (15.9500319, 37.9999668), (58.7523778, 25.3319078), (-26.5624806, 31.3991317),
                    (10.2116702, 38.6521203), (62.0448724, -7.0322972), (-51.9666424, -59.5500387),
                    (-18.1239696, 179.0122737), (63.2467777, 25.9209164), (46.603354, 1.8883335),
                    (4.0039882, -52.999998), (-17.0243749, -144.6434898), (-0.8999695, 11.6899699),
                    (13.470062, -15.4900464), (42.315407, 43.356892), (51.0834196, 10.4234469),
                    (8.0300284, -1.0800271), (36.140807, -5.3541295), (38.9953683, 21.9877132),
                    (77.6192349, -42.8125967), (12.1360374, -61.6904045), (16.2490067, -61.5650444),
                    (15.5855545, -90.345759), (10.7226226, -10.7083587), (12.100035, -14.9000214),
                    (4.8417097, -58.6416891), (19.1399952, -72.3570972), (15.2572432, -86.0755145),
                    (22.2793278, 114.1628131), (47.1817585, 19.5060937), (64.9841821, -18.1059013),
                    (22.3511148, 78.6677428), (-2.4833826, 117.8902853), (32.6475314, 54.5643516),
                    (33.0955793, 44.1749775), (52.865196, -7.9794599), (54.1936805, -4.5591148),
                    (31.5313113, 34.8667654), (42.6384261, 12.674297), (7.9897371, -5.5679458),
                    (18.1850507, -77.3947693), (36.5748441, 139.2394179), (31.1667049, 36.941628),
                    (47.2286086, 65.2093197), (1.4419683, 38.4313975), (0.3448612, 173.6641773),
                    (29.2733964, 47.4979476), (41.5089324, 74.724091), (20.0171109, 103.378253),
                    (56.8406494, 24.7537645), (33.8750629, 35.843409), (-29.6039267, 28.3350193),
                    (5.7499721, -9.3658524), (26.8234472, 18.1236723), (47.1416307, 9.5531527),
                    (55.3500003, 23.7499997), (49.8158683, 6.1296751), (22.1757605, 113.5514142),
                    (-18.9249604, 46.4416422), (-13.2687204, 33.9301963), (4.5693754, 102.2656823),
                    (4.7064352, 73.3287853), (16.3700359, -2.2900239), (35.8885993, 14.4476911),
                    (8.9995549, 168.0002575), (14.6367927, -61.01582685063731), (20.2540382, -9.2399263),
                    (-20.2759451, 57.5703566), (-12.8255515, 45.1485289522152), (23.6585116, -102.0077097),
                    (8.6062347, 151.832744331612), (47.2879608, 28.5670941), (43.73844905, 7.424224092532953),
                    (46.8250388, 103.8499736), (42.9868853, 19.5180992), (16.7417041, -62.1916844),
                    (31.1728205, -7.3362482), (-19.302233, 34.9144977), (17.1750495, 95.9999652),
                    (-23.2335499, 17.3231107), (-0.5275000000000001, 166.93479227083333), (28.1083929, 84.0917139),
                    (52.15517, 5.38721), (-21.3019905, 165.4880773), (-41.5000831, 172.8344077),
                    (12.6090157, -85.2936911), (17.7356214, 9.3238432), (9.6000359, 7.9999721),
                    (-19.0536414, -169.861341), (41.6171214, 21.7168387), (60.5000209, 9.0999715),
                    (21.0000287, 57.0036901), (30.3308401, 71.247499), (5.3783537, 132.9102573),
                    (31.462420950000002, 34.262716572130714), (8.559559, -81.1308434), (-5.6816069, 144.2489081),
                    (-23.3165935, -58.1693445), (-6.8699697, -75.0458515), (12.7503486, 122.7312101),
                    (52.215933, 19.134422), (40.0332629, -7.8896263), (25.3336984, 51.2295295),
                    (45.9852129, 24.6859225), (64.6863136, 97.7453061), (-1.9646631, 30.0644358),
                    (-21.130737949999997, 55.536480112992315), (36.638392, 127.6961188), (-15.9694573, -5.7129442),
                    (17.250512, -62.6725973), (13.8250489, -60.975036), (18.085493, -63.05129209796061),
                    (46.7775497, -56.1768672), (-13.7693895, -172.12005), (43.9458623, 12.458306),
                    (0.8875498, 6.9648718), (25.6242618, 42.3528328), (14.4750607, -14.4529612), (44.1534121, 20.55144),
                    (-4.6574977, 55.4540146), (8.6400349, -11.8400269), (1.357107, 103.8194992),
                    (18.0423736, -63.0549948), (48.7411522, 19.4528646), (45.8133113, 14.4808369),
                    (-8.7053941, 159.1070693851845), (8.3676771, 49.083416), (-28.8166236, 24.991639),
                    (7.8699431, 29.6667897), (39.3260685, -4.8379791), (7.877395849999999, 80.66247852355892),
                    (17.9036287, -62.811568843006896), (12.90447, -61.2765569), (14.5844444, 29.4917691),
                    (4.1413025, -56.0771187), (59.6749712, 14.5208584), (46.7985624, 8.2319736),
                    (34.6401861, 39.0494106), (23.9739374, 120.9820179), (38.6281733, 70.8156541),
                    (-6.5247123, 35.7878438), (14.8971921, 100.83273), (-8.5151979, 125.8375756),
                    (8.7800265, 1.0199765), (-19.9160819, -175.202642), (10.8677845, -60.9821067),
                    (33.8439408, 9.400138), (38.9597594, 34.9249653), (21.7214683, -71.6201783),
                    (-8.6405212, 179.1582918181797), (24.0002488, 53.9994829), (53.0033, -1.4701),
                    (39.7837304, -100.445882), (1.5333554, 32.2166578), (49.4871968, 31.2718321),
                    (-32.8755548, -56.0201525), (41.32373, 63.9528098), (-16.5255069, 168.1069154),
                    (41.903411, 12.4528527), (8.0018709, -66.1109318), (13.2904027, 108.4265113),
                    (-13.289402, -176.204224), (24.16819605, -13.892143025000001), (16.3471243, 47.8915271),
                    (-14.5189121, 27.5589884), (-18.4554963, 29.7468414)]

latitudes = [33.7680065, 41.000028, 28.0000272, 42.5407167, -11.8775768, 18.1954947, 17.2234721, -34.9964963,
             40.7696272, 12.51756625, -24.7761086, 47.59397, 40.3936294, 24.7736546, 26.1551249, 24.4769288, 13.1500331,
             53.4250605, 50.6402809, 16.8259793, 9.5293472, 32.30382, 27.549511, -17.0568696, 44.3053476, -23.1681782,
             -10.3333333, 18.4024395, 4.4137155, 42.6073975, 12.0753083, -3.4264997, 7.0323598, 16.0000552, 13.5066394,
             4.6125522, 61.0666922, 17.56187, 19.703182249999998, 15.6134137, 33.96579515, -31.7613365, 35.000074,
             4.099917, -12.2045176, -2.9814344, -19.919672900000002, 10.2735633, 45.5643442, 23.0131338, 12.21339425,
             34.9823018, 49.8167003, 5.178633850000001, -2.9814344, 55.670249, 11.8145966, 19.0974031, 19.0974031,
             -1.3397668, 26.2540493, 13.8000382, 1.613172, 15.9500319, 58.7523778, -26.5624806, 10.2116702, 62.0448724,
             -51.9666424, -18.1239696, 63.2467777, 46.603354, 4.0039882, -17.0243749, -0.8999695, 13.470062, 42.315407,
             51.0834196, 8.0300284, 36.140807, 38.9953683, 77.6192349, 12.1360374, 16.2490067, 15.5855545, 10.7226226,
             12.100035, 4.8417097, 19.1399952, 15.2572432, 22.2793278, 47.1817585, 64.9841821, 22.3511148, -2.4833826,
             32.6475314, 33.0955793, 52.865196, 54.1936805, 31.5313113, 42.6384261, 7.9897371, 18.1850507, 36.5748441,
             31.1667049, 47.2286086, 1.4419683, 0.3448612, 29.2733964, 41.5089324, 20.0171109, 56.8406494, 33.8750629,
             -29.6039267, 5.7499721, 26.8234472, 47.1416307, 55.3500003, 49.8158683, 22.1757605, -18.9249604,
             -13.2687204, 4.5693754, 4.7064352, 16.3700359, 35.8885993, 8.9995549, 14.6367927, 20.2540382, -20.2759451,
             -12.8255515, 23.6585116, 8.6062347, 47.2879608, 43.73844905, 46.8250388, 42.9868853, 16.7417041,
             31.1728205, -19.302233, 17.1750495, -23.2335499, -0.5275000000000001, 28.1083929, 52.15517, -21.3019905,
             -41.5000831, 12.6090157, 17.7356214, 9.6000359, -19.0536414, 41.6171214, 60.5000209, 21.0000287,
             30.3308401, 5.3783537, 31.462420950000002, 8.559559, -5.6816069, -23.3165935, -6.8699697, 12.7503486,
             52.215933, 40.0332629, 25.3336984, 45.9852129, 64.6863136, -1.9646631, -21.130737949999997, 36.638392,
             -15.9694573, 17.250512, 13.8250489, 18.085493, 46.7775497, -13.7693895, 43.9458623, 0.8875498, 25.6242618,
             14.4750607, 44.1534121, -4.6574977, 8.6400349, 1.357107, 18.0423736, 48.7411522, 45.8133113, -8.7053941,
             8.3676771, -28.8166236, 7.8699431, 39.3260685, 7.877395849999999, 17.9036287, 12.90447, 14.5844444,
             4.1413025, 59.6749712, 46.7985624, 34.6401861, 23.9739374, 38.6281733, -6.5247123, 14.8971921, -8.5151979,
             8.7800265, -19.9160819, 10.8677845, 33.8439408, 38.9597594, 21.7214683, -8.6405212, 24.0002488, 53.0033,
             39.7837304, 1.5333554, 49.4871968, -32.8755548, 41.32373, -16.5255069, 41.903411, 8.0018709, 13.2904027,
             -13.289402, 24.16819605, 16.3471243, -14.5189121, -18.4554963]

longitudes = [66.2385139, 19.9999619, 2.9999825, 1.5732033, 17.5691241, -63.0750234, -61.9554608, -64.9672817,
              44.6736646, -69.98186415210564, 134.755, 14.12456, 47.7872508, -78.0000547, 50.5344606, 90.2934413,
              -59.5250305, 27.6971358, 4.6667145, -88.7600927, 2.2584408, -64.7561647, 90.5119273, -64.9912286,
              17.5961467, 24.5928742, -53.2, -64.5661642, 114.5653908, 25.4856617, -1.6880314, 29.932395, 19.9981227,
              -24.0083947, 104.869423, 13.1535811, -107.991707, -63.138004249640304, -79.9174627243246, 19.0156172,
              -120.09189711105296, -71.3187697, 104.999927, -72.9088133, 44.2832964, 23.8222636, -157.9753368892878,
              -84.0739102, 17.0118954, -80.8328748, -69.0408499890865, 33.1451285, 15.4749544, 97.14288663046936,
              23.8222636, 10.3333283, 42.8453061, -70.3028026, -70.3028026, -79.3666965, 29.2675469, -88.9140683,
              10.5170357, 37.9999668, 25.3319078, 31.3991317, 38.6521203, -7.0322972, -59.5500387, 179.0122737,
              25.9209164, 1.8883335, -52.999998, -144.6434898, 11.6899699, -15.4900464, 43.356892, 10.4234469,
              -1.0800271, -5.3541295, 21.9877132, -42.8125967, -61.6904045, -61.5650444, -90.345759, -10.7083587,
              -14.9000214, -58.6416891, -72.3570972, -86.0755145, 114.1628131, 19.5060937, -18.1059013, 78.6677428,
              117.8902853, 54.5643516, 44.1749775, -7.9794599, -4.5591148, 34.8667654, 12.674297, -5.5679458,
              -77.3947693, 139.2394179, 36.941628, 65.2093197, 38.4313975, 173.6641773, 47.4979476, 74.724091,
              103.378253, 24.7537645, 35.843409, 28.3350193, -9.3658524, 18.1236723, 9.5531527, 23.7499997, 6.1296751,
              113.5514142, 46.4416422, 33.9301963, 102.2656823, 73.3287853, -2.2900239, 14.4476911, 168.0002575,
              -61.01582685063731, -9.2399263, 57.5703566, 45.1485289522152, -102.0077097, 151.832744331612, 28.5670941,
              7.424224092532953, 103.8499736, 19.5180992, -62.1916844, -7.3362482, 34.9144977, 95.9999652, 17.3231107,
              166.93479227083333, 84.0917139, 5.38721, 165.4880773, 172.8344077, -85.2936911, 9.3238432, 7.9999721,
              -169.861341, 21.7168387, 9.0999715, 57.0036901, 71.247499, 132.9102573, 34.262716572130714, -81.1308434,
              144.2489081, -58.1693445, -75.0458515, 122.7312101, 19.134422, -7.8896263, 51.2295295, 24.6859225,
              97.7453061, 30.0644358, 55.536480112992315, 127.6961188, -5.7129442, -62.6725973, -60.975036,
              -63.05129209796061, -56.1768672, -172.12005, 12.458306, 6.9648718, 42.3528328, -14.4529612, 20.55144,
              55.4540146, -11.8400269, 103.8194992, -63.0549948, 19.4528646, 14.4808369, 159.1070693851845, 49.083416,
              24.991639, 29.6667897, -4.8379791, 80.66247852355892, -62.811568843006896, -61.2765569, 29.4917691,
              -56.0771187, 14.5208584, 8.2319736, 39.0494106, 120.9820179, 70.8156541, 35.7878438, 100.83273,
              125.8375756, 1.0199765, -175.202642, -60.9821067, 9.400138, 34.9249653, -71.6201783, 179.1582918181797,
              53.9994829, -1.4701, -100.445882, 32.2166578, 31.2718321, -56.0201525, 63.9528098, 168.1069154,
              12.4528527, -66.1109318, 108.4265113, -176.204224, -13.892143025000001, 47.8915271, 27.5589884,
              29.7468414]


sorted_data = sorted(data.state_info(), key=lambda d: d['name'])

df = pd.DataFrame(sorted_data)
df["latitude"] = latitudes
df["longitude"] = longitudes

st.markdown("**Worldwide Data**")
st.text(f"""Worldwide Cases: {data.worldwide_cases()}
Worldwide Deaths: {data.worldwide_deaths()}
Worldwide Recoveries: {data.worldwide_recovered()}""")

st.write("")
st.write("")
country_selection = st.selectbox("View info for a specific country", data.state_list())
st.text(data.show_state_info())
st.write("")
st.write("On the map below, each dot represents a country where COVID-19 information has been collected. A larger dot represents a higher number of cases. Click a country's dot to view its cases, deaths, and recoveries")
m = folium.Map(max_bounds=True)

for index, geo_info in df.iterrows():
    opacity_for_fill = 0
    if int(geo_info["states_cases"].replace(',','')) > 10000000:
        opacity_for_fill = .5
    elif int(geo_info["states_cases"].replace(',','')) > 4000000:
        opacity_for_fill = .3
    elif int(geo_info["states_cases"].replace(',','')) > 1000000:
        opacity_for_fill = .25
    else:
        opacity_for_fill = .15

    radius_size = 0
    if int(geo_info["states_cases"].replace(',','')) < 100000:
        radius_size = int(geo_info["states_cases"].replace(',',''))/2
    elif int(geo_info["states_cases"].replace(',','')) < 1000000:
        radius_size = int(geo_info["states_cases"].replace(',',''))/8
    else:
        radius_size = int(geo_info["states_cases"].replace(',',''))/100

    folium.Circle(radius=radius_size, fill=True,
                  fill_color="#FF160C", fill_opacity=opacity_for_fill, weight=.5,
                  location=[geo_info["latitude"], geo_info["longitude"]], color="#FF160C",
                  popup=f"""{geo_info["name"]}
                  Cases: {geo_info["states_cases"]}
                  Deaths: {geo_info["states_deaths"]}
                  Recoveries: {geo_info["states_recovered"]}                 
                  """).add_to(m)
    
folium_static(m)

# Making map responsive
make_map_responsive= """
 <style>
 [title~="st.iframe"] { width: 100%}
 </style>
"""
st.markdown(make_map_responsive, unsafe_allow_html=True)
