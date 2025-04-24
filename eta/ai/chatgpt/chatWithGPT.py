from openai import OpenAI
import tiktoken

class ChatWithGPT():
    # 預設模型
    _default_model = "gpt-4o"
    # 設定匯率(新台幣/美元)
    _exc_rate = 32.5
    # 設定價格
    _price = {
        "gpt-4o":{
            "input":0.005,
            "output":0.015,
            "tokens":128000,
        },
        "gpt-3.5-turbo":{
            "input":0.0005,
            "output":0.0015,
            "tokens":16385
        }
    }

    def __init__(
            self,
            model=_default_model,
            _key="",
            max_tokens=500,
            temperature=0.5,
    ):
        self.model = model
        self._key = _key
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._messages = [
            {"role": "system", "content": "None"},
            {"role": "user", "content": "None"}
        ]


    def calculate_token_count(self, data):
        """
        計算給定資料的 token 數量。
        
        :param data: 可以是字符串 str，或是字典/列表等包含文本的資料結構
        :return: token 數量
        """
        try:
            encoding_engine = tiktoken.encoding_for_model(self.model).name
        except:
            print(f"模型名稱{self.model}錯誤無法解析")
            return
        encoding = tiktoken.get_encoding(encoding_engine)

    
        # 處理傳入的資料類型
        if isinstance(data, str):
            # 如果是字符串，直接編碼並計算 token 數量
            return len(encoding.encode(data))
        
        elif isinstance(data, list):
            # 如果是列表，遞迴計算每個元素的 token 數量
            token_count = 0
            for item in data:
                token_count += self.calculate_token_count(item)
            return token_count
        
        elif isinstance(data, dict):
            # 如果是字典，計算字典中所有值的 token 數量
            token_count = 0
            for value in data.values():
                token_count += self.calculate_token_count(value)
            return token_count
        
        else:
            # 如果不是上述任何類型，則返回 0 或拋出錯誤
            raise TypeError("Unsupported data type for token count calculation.")        

    # 設定角色
    def set_message(self, role="user", content=""):
        """
        設定AI角色以及使用者命令
        role= "system" / "user"
        content= 扮演角色 / 命令
        """
        for message in self._messages:
            if message["role"] == role:
                message["content"]=content


    def expectBill(self, text=False):
        """
        預估傳送prompt的花費，並回傳美金費用
        text: False不顯示文字
        """
        try:
            input_price = self._price[self.model]["input"] / 1000
            output_price = self._price[self.model]["output"] / 1000
        except:
            if text:
                print(f"沒有模型{self.model}的資料")
            return None
        input_tokens = self.calculate_token_count(self._messages)
        output_tokens = self.max_tokens
        input_usd = input_tokens * input_price
        input_twd = input_usd * self._exc_rate
        output_usd = output_tokens * output_price
        output_twd = output_usd * self._exc_rate

        if not text:
            return input_usd + output_usd
        
        print(f"使用的模型：{self.model}")
        print("\n預估費用：")
        print(f"輸入tokens數量:{input_tokens}", end="\t")
        print(f"{input_usd:.2f} 美金", end="\t")
        print(f"{input_twd:.2f} 臺幣", end="\t")
        print()
        print(f"輸出tokens數量:{output_tokens}", end="\t")
        print(f"{output_usd:.2f} 美金", end="\t")
        print(f"{output_twd:.2f} 臺幣", end="\t")
        print("\n")
        print("總花費 {:.2f} 美金  {:.2f}臺幣".format(
            input_usd + output_usd,
            input_twd + output_twd,
        ))

        if input_tokens + output_tokens > self._price[self.model]["tokens"]:
            print("警告！tokens過多！")
        
        return input_usd + output_usd
    
    def chat(self):
        client = OpenAI(api_key=self._key)
        response = client.chat.completions.create(
            model=self.model,
            messages=self._messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response



