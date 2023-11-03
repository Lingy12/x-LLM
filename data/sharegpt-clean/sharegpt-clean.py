# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3

import os
import json
import datasets
logger = datasets.logging.get_logger(__name__)

_CITATION = """\
@misc{alpaca,
    author = {Rohan Taori and Ishaan Gulrajani and Tianyi Zhang and Yann Dubois and Xuechen Li and Carlos Guestrin and Percy Liang and Tatsunori B. Hashimoto },
    title = {Stanford Alpaca: An Instruction-following LLaMA model},
    year = {2023},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\\url{https://github.com/tatsu-lab/stanford_alpaca}},
}
"""

_DESCRIPTION = """\
Alpaca is a dataset of 52,000 instructions and demonstrations generated by OpenAI's text-davinci-003 engine. This instruction data can be used to conduct instruction-tuning for language models and make the language model follow instruction better.

The authors built on the data generation pipeline from Self-Instruct framework and made the following modifications:
    The text-davinci-003 engine to generate the instruction data instead of davinci.
    A new prompt was written that explicitly gave the requirement of instruction generation to text-davinci-003.
    Much more aggressive batch decoding was used, i.e., generating 20 instructions at once, which significantly reduced the cost of data generation.
    The data generation pipeline was simplified by discarding the difference between classification and non-classification instructions.
    Only a single instance was generated for each instruction, instead of 2 to 3 instances as in Self-Instruct.
This produced an instruction-following dataset with 52K examples obtained at a much lower cost (less than $500). In a preliminary study, the authors also found that the 52K generated data to be much more diverse than the data released by Self-Instruct.
"""

_LANG = ["en", "es", "vi", "zh"]

class ShareGPTConfig(datasets.BuilderConfig):

    """BuilderConfig for Alpaca"""

    def __init__(self, config: str, **kwargs):
        """
        Args:
            lang: string, language for the input text
            **kwargs: keyword arguments forwarded to super.
        """
        super(ShareGPT, self).__init__(**kwargs)
        self.lang = config


class ShareGPT(datasets.GeneratorBasedBuilder):
    """This is an adapter for loading raw text parallel corpus."""
    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [ShareGPTConfig(config=lang, name=f"sharegpt-clean_{lang}") for lang in _LANG]
    BUILDER_CONFIG_CLASS = ShareGPTConfig

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "instruction": datasets.Value("string"),
                    "input": datasets.Value("string"),
                    "output": datasets.Value("string"),
                    "id": datasets.Value("string")
                }
            ),
            homepage="https://github.com/tatsu-lab/stanford_alpaca",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(self.base_path, f"platypus_{self.config.lang}.json")}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logger.info("[sharegpt] generating examples from = %s", filepath)
        
        with open(filepath, encoding="utf-8") as f:
            alpaca = json.load(f)
            id_ = 0
            for sample in alpaca:
                yield id_, sample | {"id": id_}
                id_ += 1