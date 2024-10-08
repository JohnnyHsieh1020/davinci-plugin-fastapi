from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/")
async def home(): 
    plugin = {
      "id": "HW2_API",
      "schema_version": "v1",
      "name_for_human": "HW2_API",
      "name_for_model": "HW2_API",
      "description_for_human": "This plugin helps showing student's answer and the correct answer",
      "description_for_model": "This plugin helps showing stu_ans and corr_ans",
      "auth": {
        "type": "none"
      },
      "api": {
        "type": "python",
        "python": {
          "source": "import json\nimport asyncio\nfrom pyodide.http import pyfetch\nimport sys\nimport io\nimport os\nfrom io import StringIO\nimport pandas as pd\n\n\nresponse = await chat(\n    conversation=CURRENT_CONVERSATION + [\n        {\n        \"role\": \"system\",\n        \"content\": \"Ouput the {stu_ans} then output the {corr_ans}.\"\n        }\n    ]\n)\n\n#\u6279\u6539\u4f5c\u696dfunction\nasync def compare(stu_ans, corr_ans):\n    if stu_ans:\n        print(\"Got student's answer\")\n    if corr_ans:\n        print(\"Got correst answer\")\n    return True\n\n    \nasync def main():\n    try:\n        print('CURRENT_CONVERSATION:'+str(CURRENT_CONVERSATION)) \n        try:\n            with open(SELECTED_FILES[0]['subject']) as f:\n                stu_ans=f.read()\n                print(SELECTED_FILES[0]['title'])\n                print(stu_ans)\n            \n            # \u6253API\u53d6\u5f97\u6b63\u78ba\u7b54\u6848\n            response = await pyfetch(\"https://davinci-plugin-fastapi.onrender.com/correct_answer\")\n            \n            # \u53d6\u4f3a\u670d\u5668\u7aef\u7d66\u7684\u8cc7\u6599\n            data = await response.json()\n        \n            # \u53ea\u63d0\u53d6\u6b63\u78ba\u7b54\u6848\n            filtered = data[\"corr_ans\"]\n            # \u5c07\u5b57\u4e32\u8f49\u63db\u70ba DataFrame\n            corr_ans_df = pd.read_csv(StringIO(filtered), sep=\"\\t\")\n            corr_ans = [print(row['\u7b54\u6848']) for _, row in corr_ans_df.iterrows()]\n        except Exception as ex:\n            print('SELECTED_FILES ERROR')\n\n        result = await compare(stu_ans, corr_ans)\n        if result: print(\"checked!!\")\n    except Exception as e:\n        print(f\"\u767c\u751f\u932f\u8aa4\uff1a{str(e)}\")\n\nawait main()\n"
        }
      }
    }
    

    return json.dumps(plugin)

@app.get("/correct_answer")
async def get_corr_ans():
    corr_ans = [
        '6.6	(a)-1	"C1={ ""M"":3, ""O"":3, ""N"":2, ""K"":5, ""E"":4, ""Y"":3, ""D"":1, ""A"":1, ""U"":1, ""C"":2, ""I"":1 }F1={ ""M"":3, ""O"":3, ""K"":5, ""E"":4, ""Y"":3 }C2={ ""M,O"":1, ""M,K"":3, ""M,E"":2, ""M,Y"":2, ""O,K"":3, ""O,E"":3, ""O,Y"":2, ""K,E"":4, ""K,Y"":3, ""E,Y"":2 }F2= { ""M,K"":3, ""O,K"":3, ""O,E"":3, ""K,E"":4, ""K,Y"":3 }C3= { ""M,K,O"":1, ""M,K,E"":2, ""M,K,Y"":2, ""O,K,E"":3, ""O,K,Y"":2, ""O,E,M"":1, ""O,E,Y"":2, ""K,E,Y"":2 }F3= { ""O,K,E"":3 }"',
        '6.6	(a)-2	"#1 single item frequent pattern M:3, O:3, K:5, E:4, Y:3 #2 F-list F-list: K-E-M-O-Y #3 Ordered,frequent itemlist T100 = [ K,E,M,O,Y ] T200 = [ K,E,O,Y ] T300 = [ K,E,M ] T400 = [ K,M,Y ] T500 = [ K,E,O ] #4 Conditional database of each pattern""E"" - [K:4]""M"" - [KE:2, K:1]""O"" - [KEM:1, KE:2]""Y"" - [KEMO:1, KEO:1, KM:1]"'
        '6.6	(b)	"#計算過程OKE -> O, K, E, OK, OE, KE O,K -> E (60%,100%) K,E -> O (60%,75%)  #min_conf < 80% 所以刪掉此組合 O,E -> K (60%,100%)#答案O,K -> E (60%,100%) O,E -> K (60%,100)"',
        '6.8	(a)	"#計算過程C1 = { ""Crab"":1, ""Milk"":4, ""Cheese"":3, ""Bread"":4, ""Apple"":2, ""Pie"":2 } F1 = { ""Milk"":4, ""Cheese"":3, ""Bread"":4 } C2: { ""Milk,Cheese"":3, ""Milk,Bread"":4, ""Cheese,Bread"":3 } F2 = { ""Milk,Cheese"":3, ""Milk,Bread"":4, ""Cheese,Bread"":3 } C3 = { ""Milk,Cheese,Bread"":3 } F3 = { ""Milk,Cheese,Bread"":3 }Milk,Cheese -> Bread (75%,100%) Milk,Bread -> Cheese (75%,75%)  #min_conf < 80% 所以刪掉此組合。Cheese,Bread -> Milk (75%,100) #答案 Milk,Cheese -> Bread (75%,100%) Cheese,Bread -> Milk (75%,100%)"',
        '6.8	(b)	"#計算過程C1 = { ""K-Crab"":1, ""S-Milk"":2, ""D-Cheese"":2, ""B-Bread"":1, ""W-Apple"":1, ""D-Milk"":2, ""W-Bread"":3, ""T-Pie"":2, ""B-Cheese"":1, ""G-Apple"":1}F1 = { ""S-Milk"":2, ""D-Cheese"":2, ""D-Milk"":2, ""W-Bread"":3, ""T-Pie"":2 }C2 = { ""S-Milk,D-Cheese"":2, ""S-Milk,D-Milk"":1, ""S-Milk,W-Bread"":2, ""S-Milk,T-Pie"":1, ""D-Cheese,D-Milk"":1, ""D-Cheese,W-Bread"":2, ""D-Cheese,T-Pie"":1, ""D-Milk,W-Bread"":2, ""D-Milk,T-Pie"":2, ""W-Bread,T-Pie"":2 } F2 = { ""S-Milk,D-Cheese"":2, ""S-Milk,W-Bread"":2, ""D-Cheese,W-Bread"":2, ""D-Milk,W-Bread"":2, ""D-Milk,T-Pie"":2, ""W-Bread,T-Pie"":2 }C3 = { ""S-Milk,D-Cheese,W-Bread"":2, ""D-Milk,W-Bread,T-Pie"":2 }F3 = { ""S-Milk,D-Cheese,W-Bread"":2, ""D-Milk,W-Bread,T-Pie"":2 } #答案{S-Milk,D-Cheese,W-Bread} {D-Milk,W-Bread,T-Pie}"',
        '6.14	(a)	"#計算過程s = 2000/5000 => 40%  > min_sup = 25%\ c = 2000/3000 => 66.7% > min_cof = 50% #答案Yes, this association rule is strong."',
        '6.14	(b)	"#計算過程 Lift(hot dogs,hamburgers) =  4/3 = 1.33 > 1 #答案 positively correlated"',
        '6.14	(c)	"Cosine(hot dogs, hamburgers) = 0.7303"',
        '8.6		"Naive Bayesian classification assume that attributes’ values are conditionally independent of one another, but this simplified assumption that is often unrealistic in real-world scenarios."',
        '8.12		"[1, P, 0.95] -> [1, 0, 5, 4, 0.2, 0] [2, N, 0,85] -> [1, 1, 4, 4, 0.2, 0.2] [3, P, 0.78] -> [2, 1, 4, 3, 0.4, 0.2] [4, P, 0.66] -> [3, 1, 4, 2, 0.6, 0.2] [5, N, 0.60] -> [3, 2, 3, 2, 0.6, 0.4] [6, P, 0.55] -> [4, 2, 3, 1, 0.8, 0.4][7, N, 0.53] -> [4, 3, 2, 1, 0.8, 0.6] [8, N, 0.52] -> [4, 4, 1, 1, 0.8, 0.8] [9, N, 0.51] -> [4, 5, 0, 1, 0.8, 1][10, P, 0.40] -> [5, 5, 0, 0, 1, 1]"'
    ]
    return corr_ans
    


