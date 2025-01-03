from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI
import subprocess
from qwen_agent.tools.base import BaseTool, register_tool
import json
system = ' 你是一个乐于助人小助手'

def test():
    bot = Assistant(llm={'model': 'Qwen2-7B-Instruct','model_server': ' http://localhost:8000/v1',
        'api_key': 'EMPTY',})
    messages = [{'role': 'user', 'content': [{'text': '????'}]}]
    for rsp in bot.run(messages):
        print(rsp)


@register_tool('iverilog')
class iverilogTool(BaseTool):
    # The `description` tells the agent the functionality of this tool.
    description = '运行iverilog并传递参数:param arguments: 传递的参数 :return: 输出的结果'
    parameters = [{
        'name': 'arguments',
        'type': 'array',
        # 'description': 'Detailed description of the desired image content, in English',
        'required': True
    }]
         
    def call(self, params,**kwargs) -> str:
       
        self.binary_path = './iverilog/bin/iverilog'
        try:
          
            command = [self.binary_path] + json.loads(params)['arguments']
            print(command)
  
            completed_process = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            return completed_process.stdout
        except subprocess.CalledProcessError as e:
            print(e.stderr+e.stdout)
            return f"error{e.stderr+e.stdout}"


tools = ['iverilog', 'code_interpreter']  # `code_interpreter` is a built-in tool for executing code.
files = ['/data/zhma/iverilog_quickstart.pdf']  # Give the bot a PDF file to read.
    
    
def app_gui():
    # Define the agent
    bot = Assistant(llm={ 'model': 'gpt-4o-mini','model_server': ' https://api.openai.com/v1',
        'api_key': 'your key',},
                    name='iverilog LLM-Agent',
                    #function_list=tools,
                #files=files,
                    description='自动调用iverilog工具')
    chatbot_config = {
        'prompt.suggestions': [
            {
                'text': '调用iverilog工具'
            },
        ]
    }
    WebUI(bot, chatbot_config=chatbot_config).run()#server_name="0.0.0.0"


if __name__ == '__main__':
    # test()
    app_gui()