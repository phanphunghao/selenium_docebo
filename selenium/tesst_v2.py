from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import json_utils
import json


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options)
driver.get("https://pruexpertsandboxvn.docebosaas.com/api-browser/")

time.sleep(5)

xpaths = ["""//*[@id="microservice"]/option[{}]""".format(i) for i in range(1,23)]
# services = driver.find_elements(By.XPATH, """//*[@id="microservice"]/option[.]""")
# print(len(services))

array_df = []
for xpath in xpaths:
    time.sleep(15)
    service = driver.find_element(By.XPATH, xpath)
    service_name = service.text
    print("START PROCESS SERVICE: " + service_name)
    service.click()
    time.sleep(1)
    api_refs = driver.find_elements(By.XPATH, """//*[@id="resources_nav"]/div[.]""")
    print(len(api_refs))
    
    for api_ref in api_refs:
        label = api_ref.get_attribute("label")
        print("START PROCESS API REFERENCE: " + label)
        if(label != "Home"):
            api_ref.click()
            apis = api_ref.find_elements(By.CLASS_NAME, "item")
            for api in apis:
                print("START PROCESS API: " + api.text)
                api.click()
                data_endpoint = api.get_attribute("data-endpoint")
                print("DATA ENDPOINT: " + data_endpoint)

                enpoint_method = driver.find_element(By.XPATH, f"""//*[@id="{data_endpoint}"]/*/*/*/span[@class="http_method"]""")
                print("ENDPOINT METHOD: " + enpoint_method.text)

                enpoint_path = driver.find_element(By.XPATH, f"""//*[@id="{data_endpoint}"]/*/*/*/span[@class="path"]""")
                print("ENDPOINT PATH: " + enpoint_path.text)

                if(enpoint_method.text == "GET"):
                    try:
                        _id = data_endpoint.replace(service_name+"_", "sample-", 1) + "_succes"
                        print(_id)
                        json_res = driver.find_element(By.XPATH, f"""//div[@id="{_id}"]/div[@class="snippet"]/*/code[@class="json"]""")
                        # print(json.text)
                        json_clean = json_res.text.replace("true", "\"true\"")\
                                                .replace("false", "\"false\"")\
                                                .replace("\"\"true\"\"", "\"true\"")\
                                                .replace("\"\"false\"\"", "\"false\"")
                        print(json_clean)
                        json_obj = json.loads(json_clean)
                        # print(json_obj)
                        json_flatten = json_utils.flatten_json(json_obj)
                        print(json.dumps(json_flatten))
                        # ====================================== PROCESSING PANDAS DF ======================================
                        df = pd.json_normalize(json_flatten)
                        print(df.columns.values)
                        data = []
                        for col in df.columns.values:
                            data.append([
                                            service_name
                                            ,enpoint_method.text + " | " + enpoint_path.text
                                            ,col
                                        ])
                        create_df = pd.DataFrame(data, columns=["API", "endpoint", "parsing"])
                        print(create_df)
                        array_df.append(create_df)
                    except Exception as e:
                        exception_df = pd.DataFrame([[service_name, enpoint_method.text + " | " + enpoint_path.text, e]], columns=["API", "endpoint", "exception"])
                        exception_df.to_csv("exception/" + api.text + ".txt", sep='\t', index=False)
                        continue
                else:
                    pass
    print("END PROCESS SERVICE: " + service_name)
    
if(len(array_df) !=0):
    print(len(array_df))
    result_df = pd.concat(array_df)
    result_df.to_csv("output/decebo.csv", index=False)
else: 
    pass

time.sleep(10)
driver.close()
