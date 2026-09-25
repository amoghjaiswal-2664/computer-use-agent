import json
from agent.llm import _client
from agent.tools import tools, call_tool
from agent.computer import take_screenshot
import base64
def encode_image(path: str)->str:
    with open(path,"rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
def screenshot_message(path: str, caption: str = "Here is a screenshot after that action:"):
    b64 = encode_image(path)
    return {
        "role": "user",
        "content": [
            {"type": "text", "text": caption},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{b64}"
                },
            },
        ],
    }
def strip_old_images(messages: list, keep_last: int = 1)-> list:
    """
    Replace image content in all but the most recent `keep_last` image messages
    with a lightweight text placeholder, to keep token usage bounded.
    """
    image_indices = [
        i for i, m in enumerate(messages)
        if isinstance(m.get("content"),list)
        and any(block.get("type")=="image_url" for block in m["content"])
    ]
    indices_to_strip = image_indices[:-keep_last] if keep_last > 0 else image_indices

    for i in indices_to_strip: 
        messages[i] = {
            "role": messages[i]["role"],
            "content": "[earlier screenshot omitted to save tokens]",
        }
    return messages
def summaraize_step(tool_name: str, args: dict, result, step) -> str:
    """
    summarize messages by removing excess info about tools history 
    """
    status = "FAILED" if str(result).startswith("ERROR:") else "succeeded"
    summary = f"{step}: {tool_name}:{args} and {status}"    
    return summary        
def run(goal: str,model: str = "qwen/qwen3.8-27b", max_steps: int=10 ):
    messages = [{"role":"user", "content":goal}]
    done = False
    step = 0
    while not done and step<max_steps:
        response = _client.chat.completions.create(
            model = model,
            max_tokens=512,
            messages=messages,
            tools = tools,
            tool_choice="auto",
            reasoning_effort="none",
            reasoning_format="hidden",
        )
        message = response.choices[0].message
        if message.tool_calls:
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [tc.model_dump() for tc in message.tool_calls] if message.tool_calls else None,
            })

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                print(f"Steps{step}: calling {name}({args})")
                
                try:
                    result = call_tool(name, args)
                except Exception as e:
                    result = f"ERROR: {e}"

                screenshot_path = take_screenshot(f"step_{step}.png")
                
                messages.append({
                    "role":"tool",
                    "tool_call_id":tool_call.id,
                    "content":summaraize_step(name, args, result,step),
                })
                messages.append(screenshot_message(screenshot_path))
                messages = strip_old_images(messages, keep_last=1) 
        else:
            print("Agent:",message.content)
            done = True
        step += 1

    if step >= max_steps and not done:
         print("Hit max_steps without finishing.")
        

