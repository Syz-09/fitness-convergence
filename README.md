# Global Fitness Convergence?

[English](#english) · [中文](#中文)

## English

**A quantitative comparison of fitness themes in trending videos across countries.**

Are exercise practices, body ideals, and wellness consumption becoming more alike across countries? This broad question has no single ready-made measure. This project takes a narrower, measurable first step: it asks whether **fitness-related trending videos** emphasize similar themes in different countries. Video titles are classified into four overlapping dimensions—**workout, body, nutrition, and wellness**. The prevalence of each theme forms a four-dimensional country profile. Cosine similarity compares the profiles, while bootstrap resampling shows how sensitive the comparisons are to the available videos.

> **Scope of the evidence:** The included results use **36 synthetic example videos** from Germany, India, and Pakistan to demonstrate the analysis pipeline. They do not establish real-world cultural convergence. The current implementation compares one static sample; it does not measure change over time or analyze health statistics or consumer spending.

### Research workflow

1. **Prepare the data:** Match alternative column names for titles, countries, views, likes, and comments; remove invalid and duplicate records.
2. **Define measurable themes:** Use title keywords to label workout, body, nutrition, and wellness content. A video can belong to more than one theme.
3. **Represent each country:** Compute the share of fitness-related videos and a four-dimensional vector of theme prevalence within those videos. The vector components need not add up to one.
4. **Compare and test stability:** Calculate cosine similarity between country vectors. Resample fitness-related videos within each country 300 times to obtain empirical similarity intervals.
5. **Explore engagement:** Fit a logistic regression model to test whether country and simple title features help predict engagement above each country's median.

### Results from the synthetic example

| Country pair | Cosine similarity | Bootstrap mean | Empirical 95% interval |
| --- | ---: | ---: | ---: |
| India–Pakistan | 0.994 | 0.828 | [0.465, 0.979] |
| Germany–Pakistan | 0.867 | 0.714 | [0.269, 0.981] |
| Germany–India | 0.823 | 0.686 | [0.263, 0.979] |

Each country has 12 example videos, nine of which are labeled fitness-related. India and Pakistan have the highest point similarity, but the bootstrap intervals are wide and overlap, so the ordering is uncertain. The exploratory engagement model scores 0.636 accuracy, 0.667 balanced accuracy, and 0.633 ROC–AUC on 11 test records. This small experiment does not support strong predictive or causal claims. See the [full research report](Report_Fitness.pdf) for methods, figures, and interpretation.

![Cosine similarity between country profiles](results/figures/country_similarity_notebook.png)

### Repository contents

| Path | Contents |
| --- | --- |
| [`fitness_convergence.ipynb`](fitness_convergence.ipynb) | Interactive analysis from example data to figures |
| [`src/`](src/) | Data validation, preprocessing, topic profiles, similarity, modeling, and visualization functions |
| [`data/sample/mini_fixture.csv`](data/sample/mini_fixture.csv) | 36 synthetic example records |
| [`data/processed/`](data/processed/) | Cleaned data and country-level measures from the example run |
| [`results/`](results/) | Example metrics, bootstrap results, and figures |
| [`Report_Fitness.pdf`](Report_Fitness.pdf) | Full research report in English |

### Run the notebook

Use Python 3.10+ and Jupyter Notebook or a compatible notebook environment.

```bash
python -m pip install -r requirements.txt
python -m pip install jupyterlab
jupyter lab fitness_convergence.ipynb
```

Run the cells in order from the repository root. The default setting, `USE_PUBLIC_DATA = False`, uses the included synthetic sample. The notebook writes outputs to `data/processed/` and `results/`. Before using external data, verify column definitions, country labels, sampling dates, platform coverage, and usage rights. The external repository URL in `src/config.py` is a data entry point that still requires validation for this research question.

### Interpretation and next steps

- Title keywords measure the **visibility of online themes**. They do not directly measure exercise behavior, body ideals, wellness purchases, or health outcomes.
- Cosine similarity describes the relative structure of four themes, not equality in content volume, participation, or health.
- Testing whether countries are **converging over time** requires comparable samples from multiple periods, consistent measures of between-country distance, and sensitivity checks using alternative keywords, scaling choices, and data sources.
- Any later analysis of wellness consumption or health outcomes should model those measures separately from online attention and explain the different meanings of the indicators.

## 中文

**跨国健身内容的量化比较。**

不同国家的健身方式、身体审美和健康消费是否正在趋同？这个宽泛问题没有现成的统一指标。本项目先研究其中一个可测量的部分：**各国热门视频中的健身内容是否具有相似的主题结构**。分析将视频标题归纳为 **训练、体态、营养、身心健康** 四个可重叠的维度，以各主题在本国健身视频中的出现比例构成国家向量，再用余弦相似度比较国家之间的主题分布，并通过自助重采样检查结果对样本变动的敏感程度。

> **研究范围**：仓库中的结果来自德国、印度、巴基斯坦共 36 条**合成示例视频**，用于演示和验证分析流程。它们不能证明现实中的健身文化已经趋同。当前实现比较的是一个静态样本，没有估计随时间变化的趋同趋势，也没有使用健康统计或消费数据。

### 研究流程

1. **整理数据**：识别不同命名的标题、国家、观看量、点赞量、评论量等字段，清除无效值和重复记录。
2. **构建指标**：按标题关键词给视频标记训练（workout）、体态（body）、营养（nutrition）、身心健康（wellness）主题；一条视频可属于多个主题。
3. **表示国家**：计算每个国家的健身相关视频占比，以及四维主题向量。向量分量是各主题在本国健身视频中的出现比例，因此不要求相加为 1。
4. **比较与验证**：计算国家向量之间的余弦相似度，并在各国内对健身视频进行 300 次自助重采样，报告相似度的经验区间。
5. **探索互动量**：以各国互动率中位数为界，建立一个逻辑回归模型，探索国家与标题特征能否预测相对较高的互动量。

### 示例结果

| 国家组合 | 主题向量余弦相似度 | 重采样均值 | 95% 经验区间 |
| --- | ---: | ---: | ---: |
| 印度–巴基斯坦 | 0.994 | 0.828 | [0.465, 0.979] |
| 德国–巴基斯坦 | 0.867 | 0.714 | [0.269, 0.981] |
| 德国–印度 | 0.823 | 0.686 | [0.263, 0.979] |

三个国家各有 12 条示例视频，其中各有 9 条被关键词规则标为健身相关。点估计显示印度与巴基斯坦的主题向量最接近，但重采样区间宽且相互重叠，应谨慎解释排序。探索性互动模型在 11 条测试记录上的准确率为 0.636，平衡准确率为 0.667，ROC–AUC 为 0.633；该小样本实验不支持强预测或因果结论。详细方法、图表和解释见 [研究报告](Report_Fitness.pdf)。

### 仓库内容

| 路径 | 内容 |
| --- | --- |
| [`fitness_convergence.ipynb`](fitness_convergence.ipynb) | 从示例数据到图表的完整交互式分析 |
| [`src/`](src/) | 字段验证、预处理、主题表示、相似度、模型与可视化函数 |
| [`data/sample/mini_fixture.csv`](data/sample/mini_fixture.csv) | 36 条合成示例记录 |
| [`data/processed/`](data/processed/) | 示例运行生成的整理后数据与国家指标 |
| [`results/`](results/) | 示例指标、重采样结果与图表 |
| [`Report_Fitness.pdf`](Report_Fitness.pdf) | 完整英文研究报告 |

### 运行

需要 Python 3.10+、Jupyter Notebook 或兼容的笔记本环境。

```bash
python -m pip install -r requirements.txt
python -m pip install jupyterlab
jupyter lab fitness_convergence.ipynb
```

从仓库根目录运行笔记本，按顺序执行单元。默认 `USE_PUBLIC_DATA = False`，使用仓库内的合成示例数据。笔记本会写入 `data/processed/` 和 `results/`。若改用外部数据，需先核对字段、国家含义、采样时间、平台覆盖范围与数据使用许可；`src/config.py` 中的外部数据仓库地址仅提供一个待核验的数据入口。

### 解释边界与下一步

- 标题关键词衡量的是**网络内容的主题可见度**，不能直接代表真实锻炼行为、身体审美、健康消费或健康水平。
- 余弦相似度比较的是四类主题的相对结构，不表示两个国家的内容量、参与率或健康状况相同。
- 要回答“是否正在趋同”，需要有可比的跨期样本，在统一口径下比较各时间点的国家间距离，并用替代关键词、标准化方法与其他数据源检验稳定性。
- 若进一步研究健康消费或健康结果，应将其与网络内容指标分开建模，并在解释中明确两类指标的不同含义。
