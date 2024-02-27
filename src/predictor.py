from peft import PeftConfig, AutoPeftModelForCausalLM
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Predictor:
    def __init__(self, model_load_path: str):
        self.model = AutoModelForCausalLM.from_pretrained(
                            model_load_path,
                            low_cpu_mem_usage=True,
                            torch_dtype=torch.float16,
                            load_in_8bit=True,
                            device_map='auto',
                        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_load_path)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
     

    def get_input_ids(self, prompt: str):
        
        input_ids = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
            ).input_ids.cuda()
        return input_ids

    @torch.inference_mode()
    def predict(self, prompt: str, max_target_length: int = 150, temperature: float = 0.7) -> str:
        input_ids = self.get_input_ids(prompt)
        outputs = self.model.generate(
            input_ids=input_ids,
            do_sample=True,
            top_p=0.95,
            max_new_tokens=max_target_length,
            temperature=temperature,
        )
        prediction = self.tokenizer.batch_decode(outputs.cpu().numpy(), skip_special_tokens=True)[0]

        return prediction
    
if __name__ == '__main__':
    
    path = '/root/kodkobzar/KodKobzar/src/models/kodkobzar13B_x2_lit_history_lang_finetuned/assets'
    predictor = Predictor(model_load_path=path)
   
    # prediction = predictor.predict(prompt="USER:  Стоїцизм був впливовим філософським напрямком від епохи раннього еллінізму аж до кінця античного світу. Свій вплив ця школа залишила і на подальші філософські епохи. ASSISTANT: ")
    # print(prediction)
    # print()
    # prediction = predictor.predict(prompt="USER: Украї́на — держава, розташована у Східній та частково у Центральній Європі, охоплює південний захід Східноєвропейської рівнини, частину Східних Карпат і Кримські гори. ASSISTANT: ")
    # print(prediction)
    # print()
    prediction = predictor.predict(prompt="USER: Яке місто в Україні називають найромантичнішим? ASSISTANT: ")
    print(prediction)