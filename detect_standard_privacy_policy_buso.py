import asyncio
import csv
import json
import openai
import os
from dotenv import load_dotenv


class HANDLER:
    @staticmethod
    def remove_empty_lines(content):
        lines = content.split("\n")
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return "\n".join(cleaned_lines)

    @staticmethod
    def ask_gpt(privacy_policy_content):
        try:
            prompt_message = [
                {
                    "role": "system",
                    "content": "You are an expert in classifying privacy policy documents provided by Android applications as Good Standard or Bad Standard, based on the set of definitions below.\n\n– Firstly, the principle of lawfulness demands that all data processing must have a legitimate basis, be it through the consent of the data subject, the ne- cessity for the performance of a contract, compliance with a legal obligation, protection of vital interests, performance of a task carried out in the public interest, or for the purposes of legitimate interests pursued by the data con- troller or a third party. This principle insists on a legal foundation for data processing activities, ensuring that they are not arbitrary but grounded in law and necessity.\n– Closely tied to lawfulness is the principle of fairness. This principle ensures that the processing of data does not detrimentally affect the rights and free- doms of the individual. It calls for transparency and honesty in how data is handled, ensuring that individuals are not misled or manipulated regarding the use of their personal data.\n– Transparency is another cornerstone of GDPR, which necessitates clear, open, and honest communication with data subjects about how their data is being processed. This principle compels organizations to provide accessible information about their data processing activities and to make this informa- tion understandable to the average person, not shrouded in legal jargon.\n– The principle of purpose limitation requires that data be collected for specified, explicit, and legitimate purposes and not further processed in a manner that is incompatible with those purposes. This principle limits the scope of data use, ensuring that organizations do not repurpose data for unrelated or illegitimate activities.\n– Data minimization is a call for restraint; it demands that the personal data collected should be adequate, relevant, and limited to what is neces- sary in relation to the purposes for which they are processed. This principle challenges the culture of excess data collection, promoting a more considered and conservative approach to data acquisition.\n– Ensuring the accuracy of personal data is another critical aspect of GDPR. It requires organizations to take every reasonable step to ensure that per- sonal data that are inaccurate, considering the purposes for which they are processed, are erased or rectified without delay. This principle upholds the integrity of personal data and the decisions made based on this data.\n– Storage limitation asserts that personal data should be kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed. This principle en- courages organizations to regularly review their data and dispose of anything that is no longer required.\n– Lastly, the principles of integrity and confidentiality mandate that per- sonal data must be processed in a manner that ensures appropriate secu- rity, including protection against unauthorized or unlawful processing and against accidental loss, destruction, or damage, using appropriate techni- cal or organizational measures. This principle is the bedrock of trust in the digital ecosystem, ensuring that data is not only used responsibly but also safeguarded with utmost diligence.\n\nI. Good Privacy Policy Standards: The criteria for good privacy policy stan- dards are directly derived from the GDPR Article 5 principles. A privacy policy that adheres well to these standards is one that demonstrates lawfulness, fair- ness, and transparency in data processing activities. This means that the policy clearly states the legal basis for processing data, such as user consent or legiti- mate interest, and ensures that the data processing does not unjustly affect the data subject. It should be transparent about how data is collected, used, shared, and stored, providing clear, accessible information that is easy for the average user to understand.In terms of purpose limitation, a strong privacy policy will specify the exact purposes for data collection and assert that data will not be used in a manner incompatible with these purposes. It should demonstrate data minimization by collecting only the data that is necessary for the stated purposes and no more. The policy should also emphasize the accuracy of data, detailing the measures in place to ensure that personal data is kept up to date and accurate.A good privacy policy will also address storage limitation, indicating the time period for which the data will be stored and the criteria used to deter- mine this duration. It should assure users of the integrity and confidentiality of their data, outlining the security measures implemented to protect data against unauthorized access, accidental loss, destruction, or damage.\nII. Bad Privacy Policy Standards: On the flip side, indicators of bad privacy policy standards are largely characterized by non-compliance or poor practices in relation to GDPR Article 5 principles. For example, a policy that lacks a clear legal basis for data processing, uses vague language, or engages in processing activities that could be deemed unfair or non-transparent would be considered deficient. Such a policy might obscure the details about data use or share data with third parties without explicit user consent, failing to uphold the principle of transparency.A privacy policy that allows for the excessive collection of data, well beyond what is necessary for the stated purposes, would be flagged negatively under the data minimization criterion. Similarly, policies that do not provide mechanisms for ensuring the accuracy of data, or fail to allow users to easily rectify or update their information, would fall short of the accuracy standard. Policies that do not specify the retention period of the data or retain data indefinitely without a legitimate reason would violate the storage limitation prin- ciple. A lack of robust security measures to protect data, or the absence of clear protocols for responding to data breaches, would indicate a failure to ensure data integrity and confidentiality.",
                },
                {
                    "role": "user",
                    "content": "Based on the content of the privacy policy below. Please conclude whether the content is Good Standard or Bad Standard ? (NOTE: Please give the result as: | Good or Bad | The reason is brief, giving specific sections ...)\n\n"
                    + privacy_policy_content,
                },
            ]
            response = openai.ChatCompletion.create(
                model=os.getenv("MODEL_GPT4"), messages=prompt_message
            )
            assistant_reply = response.choices[0].message["content"]
            return assistant_reply
        except Exception as e:
            return "Error: The prompt length exceeds the maximum allowed length of 8192 tokens."

    @staticmethod
    async def loop_csv(input_csv_path, output_csv_path):
        with open(input_csv_path, "r", newline="", encoding="utf-8") as csvfile, open(
            output_csv_path, "w", newline="", encoding="utf-8"
        ) as outputfile:

            reader = csv.reader(csvfile)
            writer = csv.writer(outputfile)

            headers = next(reader)
            writer.writerow(headers)

            for index, row in enumerate(reader):
                print(
                    "\n_____________ Run times "
                    + str(index + 1)
                    + " <"
                    + row[1]
                    + "> "
                    + "_____________"
                )
                gpt_result = HANDLER().ask_gpt(row[10])
                row[headers.index("standard_reason")] = HANDLER().remove_empty_lines(
                    gpt_result
                )
                writer.writerow(row)
                print("~~~~~~~~~~~~~~ Success ~~~~~~~~~~~~~~\n")


async def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    input_csv_path = "./list_app_business2.csv"
    output_csv_path = "./list_app_business3.csv"

    await HANDLER().loop_csv(input_csv_path, output_csv_path)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
