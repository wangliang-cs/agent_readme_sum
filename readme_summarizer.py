from openai import OpenAI


class ReadmeSummarizer:
    def __init__(self, api_key_file):
        """Initialize the ReadmeSummarizer with OpenAI API key."""
        self.api_key = None
        try:
            with open(api_key_file, "r") as fd:
                self.api_key = fd.readline().strip()
        except Exception as e:
            print(e)

        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

    import re

    def extract_functional_description(self, readme_text):
        # 定义可能包含功能描述的关键词
        keywords = ["功能", "特性", "features", "functionality", "description"]

        # 将README文本按段落分割
        paragraphs = readme_text.split('\n\n')

        # 查找包含关键词的段落
        functional_description = []
        for paragraph in paragraphs:
            if any(keyword.lower() in paragraph.lower() for keyword in keywords):
                functional_description.append(paragraph)

        # 如果没有找到相关段落，返回整个README
        if not functional_description:
            return readme_text

        return "\n\n".join(functional_description)

    def summarize(self, readme_content: str) -> str:
        """
        Summarize the functionality described in a README file using OpenAI's GPT model.
        
        Args:
            readme_content (str): The content of the README file to summarize
            
        Returns:
            str: A concise summary of the README's functionality
        """
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system",
                     "content": "You are a technical documentation expert. Summarize the key functionality described "
                                "in this README file concisely with a single paragraph, no more than 250 words, "
                                "and in English. Do not include information that are not about functionality, "
                                "like contributors or license, etc. Respond in plain text, no markdown symbols."},
                    {"role": "user", "content": readme_content}
                ],
                max_tokens=200,
                # temperature=0.7,
                stream=False
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

    def summarize_from_file(self, file_path: str) -> str:
        """
        Read a README file and summarize its functionality.
        
        Args:
            file_path (str): Path to the README file
            
        Returns:
            str: A concise summary of the README's functionality
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return self.summarize(content)
        except FileNotFoundError:
            raise FileNotFoundError(f"README file not found at {file_path}")
        except Exception as e:
            raise Exception(f"Error reading or processing file: {str(e)}")

    def extract_from_file(self, file_path: str) -> str:
        """
        Read a README file and summarize its functionality.

        Args:
            file_path (str): Path to the README file

        Returns:
            str: A concise summary of the README's functionality
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return self.extract_functional_description(content)
        except FileNotFoundError:
            raise FileNotFoundError(f"README file not found at {file_path}")
        except Exception as e:
            raise Exception(f"Error reading or processing file: {str(e)}")


if __name__ == "__main__":
    rs = ReadmeSummarizer("../agent_readme_sum_data/deepseek_api_key.txt")
    # summ_txt = rs.summarize_from_file("../agent_readme_sum_data/readme/README_tensorflow.md")
    # summ_txt = rs.summarize_from_file("../agent_readme_sum_data/readme/README_pytorch.md")
    summ_txt = rs.extract_from_file("../agent_readme_sum_data/readme/README_tensorflow.md")
    # summ_txt = rs.extract_from_file("../agent_readme_sum_data/readme/README_pytorch.md")
    print(summ_txt)
