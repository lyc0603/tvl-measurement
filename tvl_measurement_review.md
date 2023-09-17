# TVL measurement review

## General Comments

- [ ] i still think the sankey plot is interesting - especially given that we lack interesting / sophisticated visualization in the paper. but indeed, one sankey plot might be too week -- a couple of sankey plots from different, representative points in time would be more powerful. but if you can come up with better visualization, we can also deprecate the sankey plots

- [ ] also, again in general many plots take too much space - giving reviewer the impression of low cost (as in space-taking)  benefit ratio. Reducing the plot size helps as well

## WINE

-------------------------  METAREVIEW  ------------------------
The question of what is the right metric to measure how users value a protocol is an interesting one, but the present paper is far from something that is publishable in WINE. A few thoughts for the author(s):

1. Is an outlet like WINE the correct outlet for such a paper? I would argue no---maybe a more industry focused outlet would be appropriate.

- [ ] 2. If an outlet like WINE is the desired outlet, the reveiwers unanimously feel that more formalism would be useful: for example a formal model of what a metric like TVL/ TVR is meant to measure, more exact definitions, connections to the literature etc.

Overall I suspect route 1 might be the better path for this paper. Either way I hope the author(s) use the feedback of the reviewers which was farily unanimous and I concur with.

> YC: Highlight the necessity of TVR framework via comparing the risk of TVL and TVR frameworks. For example, the existance of derivatve tokens under the TVL framworks will inflate the withdrawable value and might cause the snowballing effect.

----------------------- REVIEW 1 ---------------------
SUBMISSION: 6034
TITLE: Deceit in DeFi: Unlocking Total Value Locked
AUTHORS: Yichen Luo, Yebo Feng, Antoine Mouran and Jiahua Xu

----------- Overall evaluation -----------
Summary: The paper argues that the metric of Total Value Locked (TVL) to measure the "size" of the DeFi market is flawed since it double-counts the value of tokens in interconnected protocols or in derivative tokens. Specifically, the paper argues that DeFiLlama's metric of TVL without double counting is still flawed and inflated. As a remedy, it proposes the metric of Total Value Redeemable (TVR) which only counts the amount of tokens (value) that investors can withdraw at a given time, thus, avoiding the double-counting problem. On the Ethereum mainnet, the redeemable tokens include Ether, governance tokens, wrapped tokens, and non-crypto-backed (NCB) stablecoins.

- [ ] The paper uses data from 7 popular protocols (including Aave V2, Balancer, MakerDAO, Uniswap V2, Compound V2 among others) on a single block that was mined on May-22-2023 to demonstrate the actual decomposition of the TVL and TVR in the DeFi ecosystems and then presents data between 2019 and 2023 that show the time series of TVL, TVL without double counting (DeFiLlama's improved metric) and TVR. It is not entirely clear how was this data collected.

> YC: Polish the description of data collection part.

- [ ] Evaluation: The paper is hard to understand and I think that the exposition is not detailed enough. For instance, there are no rigorous definitions of TVL, TVL without double counting and not even of the proposed metric TVR. One needs to search in the text to find it, but even then, this is not clear. There are several others obscure points in the paper:

> YC: Add formal definitions of TVL and TVL without double counting via references.

- [ ] what is the point of the analysis of a single block 

> YC: Remove the sankey plot (already have time-series) and fetch the timeseries of token composition of key protocols.

- [ ] and where does the data for the time-series (in Fig5) come from? 

> YC: Further clarify the data collection process of time-series.

- [ ] Some numbers are difficult to verify: e.g., the paper argues that up to 25.7% of DeFiLlama's TVL without double counting is still due to double counting but Figure 3 shows a number of 64.8%. Does this refer to Double Counting with the naive TVL metric? This is unclear and very confusing.

> YC: Can remove this cross-sectional data due to the existance of time-series

- [ ] how is it possible that the blue line is above the yellow line in Figure 5 (c) Binance and (h) Mixin? Isn't the blue line a "subset" of the yellow line?

> YC: Should check the data (highly likely to be the DeFillama data error, one flaw of defillama).

- [ ] The paper is not well written and contains repetitive passages, e.g., "We collect the amount..." or statements, e.g., that the new metric is useful to investors, even in the same paragraph (Conclusions).

> YC: Remove duplications.

- [ ] In addition, much of the content of the paper is not novel material, e.g., the examples of double counting which is a known problem and the lengthy discussions and literature review. 

> YC: Shorten the literature review and discussions.

Finally, apart from not being clear with its methodology, the paper seems to achieve a contribution of limited scope at the current moment - although the introduction of the new metric is definitely an interesting topic to research. This is because, there is no evidence that this metric is actually correct or more accurate representation of the total value locked or at a risk in the DeFi ecosystem at a given moment.

In sum, I think that the paper needs to be thoroughly revised to include rigorous definitions of its metrics and testable arguments of its claims. Also, the exposition needs to be improved before the paper is ready for publication. However, the topic is interesting and the paper can make potentially a valid contribution to the literature. That is why, I encourage the authors to continue working on this topic.



----------------------- REVIEW 2 ---------------------
SUBMISSION: 6034
TITLE: Deceit in DeFi: Unlocking Total Value Locked
AUTHORS: Yichen Luo, Yebo Feng, Antoine Mouran and Jiahua Xu

----------- Overall evaluation -----------
Summary:
The paper presents a novel approach to measuring the value locked in the DeFi system, introducing the Total Value Redeemable (TVR) framework aimed at mitigating TVL double counting. The methodology leans on the double-entry bookkeeping principle from accounting to address the perceived inaccuracies of TVL computations. While the underlying concept of eliminating double counting is significant, the paper suffers from a lack of clarity, questionable design choices, inadequate data analysis, and unrelated references.

Key Concerns:

- [ ] Ambiguous Research Motivation: The paper doesn’t effectively establish the need for the study. It hints at "double counting" challenges in the first page's final paragraph but fails to explain the nuances of this issue in the DeFi context or its broader implications.

> YC: Add the motivation of TVR framework via comparing the risk of TVL and TVR frameworks. For example, the existance of derivatve tokens under the TVL framworks will inflate the withdrawable value and might cause the snowballing effect.

- [ ] Inadequate Solution to Double Counting: The TVR, as delineated, doesn't seem to truly address double counting; rather, it appears to sidestep it. The mention in the third section that "TVR exclusively considers the ultimate source token, neglecting receipt or derivative tokens" suggests a potential oversimplification rather than a resolution.

> YC: Possibly add the balance sheet elimination method?

- [ ] Misplaced Data Analysis: The data analysis seems to emphasize the importance of addressing TVL double counting more than it does the efficacy of the TVR. This could be better suited to the motivation section.

> YC: Add the motivation section.

- [ ] Moreover, the presentation of data lacks transparency. Figure 3, for instance, offers percentages without context or explanation, and the rationale for using a time series in section 4.4 remains ambiguous.

> YC: Elaborate more on the percentage and time-series.

- [ ] Irrelevant Related Work: The literature review section could be more discerning. The referenced works don't seem closely related to TVL computation methodologies. Instead of drawing parallels or highlighting gaps in previous studies, the paper merely lists paper overviews, occupying excessive space without adding value.

> YC: Add more literature in the traditional finance and economics.

Presentational Issues: There are various presentation errors which mar the paper’s quality:

Typographical error in "Collatized" in section 2.1's ninth line.
Inconsistencies in naming, such as "aDAI" and "DAi" in place of DAI, observed in section 2.5's second paragraph.
Reference mistakes, notably the incorrect table citation on the sixth page's last line, which should point to Table 2c.
Repetitive content in section 3.3, where the first two paragraphs are identical.
Erroneous image referencing in section 4.4's initial sentence, which should cite Figure 6.

> YC: Need thorought proofreading.

Despite its attempts to address a timely issue in the DeFi ecosystem, the paper's shortcomings are too numerous to overlook. For these reasons, the paper does not meet the acceptance criteria. Future submissions would benefit from a more rigorous approach to problem definition, solution articulation, and data analysis.



----------------------- REVIEW 3 ---------------------
SUBMISSION: 6034
TITLE: Deceit in DeFi: Unlocking Total Value Locked
AUTHORS: Yichen Luo, Yebo Feng, Antoine Mouran and Jiahua Xu

----------- Overall evaluation -----------
The authors study the limitations of using Total Value Locked (TVL) as a metric for on-chain economic activity, and propose the Total Value Redeemable (TVR) instead. Given that many different tokens can co-exist on a blockchain, quantifying the monetary value of all those assets is tricky, especially given than many of them are derivatives of others, or might be locked into smart contracts. TVL is not formally defined (either in the paper or otherwise) and largely open to interpretation, but could lead to some double counting, especially with respect to derivative tokens: one could deposit token A to borrow token B (which is newly minted) and then use token B to mint token C. Depending on the definition of TVL, either A. + B + C, or B + C or just C, or just A could all be valid answers, based on the way derivatives and locked tokens are counted.

The proposer TVR metric only counts (e.g. on Ethereum) ETH, governance tokens, wrapped tokens and non-crypto-backed stablecoins. The authors then collect data to show that indeed TVR is lower than a common interpretation of TVL, including a variation offered by CoinLlama which is TVL without double counting.

While the goal of improving TVL as a metric is commendable, I think the current approach is exploratory in nature and primarily highlights that TVL has many issues without offering a more comprehensive framework of what constitutes on chain value creation and how it should be counted. 

- [ ] The TVR metric, although potentially more useful, has no rigorously defined financial underpinnings supporting why it is a better choice. 

> YC: Use the risk analyses to clarify the benefit of TVR over TVL.

Finally, I am not sure if WINE is the right target conference for this type of paper (at least it would need a formal model explaining how value is driven on-chain, even if there are no rigorous results outside of data analysis).

Specific comments:

- [X] Why is so much text in italics in 2.3?

> YC: Remove the italics.

- [ ] About DefiLlama, on page 3: “Furthermore, assets generated by one protocol and locked in another protocol are only counted in the TVL of the latter protocol”. But then the example about AAVE seems to do this.

> YC: DeFiLlama does not actually adopt this method. Should clarify more on this.

- [ ] A better definition of what a derivative token is in page 9. I am not sure if this approach can cover all available token derivatives.

> YC: Should make the explanation more persuative maybe?

## ACM

Review #159A
===========================================================================

Recommendation
--------------
1. Reject

Novelty
-------
1. Not applicable - paper is for replicability track

Contribution made by replication/reproduction
---------------------------------------------
1. Not applicable - paper is not for replicability track

Value to the community
----------------------
1. No value

Reproducibility
---------------
3. Most of the work can be reproduced

Supplementary material
----------------------
1. No supplementary material

Writing quality
---------------
3. Adequate

Reviewer expertise
------------------
1. No familiarity

Paper summary
-------------
This paper identifies the problem of double counting value in decentralized finance (DeFi) systems and describes a measurement approach to avoid double counting. The results show that the actual value is 74% of the total value locked.

Reasons to accept
-----------------
The paper provides good background into DeFi applications and sheds light on the nature of the double counting problem. Accurately accounting for total value of the system without double counting is important.

Reasons to reject
-----------------
- [ ] There isn't very deep analysis of the results. There is <1 page worth of results with plenty of room left in the paper (it's only 9 pages). There should have been a much deeper analysis of the results.

> YC: Add risk analyses as well as more sophisticated figures.

Comments for authors
--------------------
- [ ] What was the reasoning for choosing these 7 DeFi protocols for evaluation in this paper? Please add some context for readers that may be unfamiliar with these applications.

> YC: Possibly remove these seven protocols.

The results section is overly brief. I would have liked to see a much deeper analysis into the collected results rather than just reporting the data. The results section is <1 page and there is plenty of space left in the paper to provide deeper analysis.

I was left wondering what the implications of these results are, how the results should be used, and by whom? Who is the target audience? Is a single snapshot of these findings actionable by the concerned parties, or do we need continuous ongoing measurements?

- [ ] paper formatting: the header shows "CoNEXT ’18, December 4–7, 2018, Heraklion/Crete, Greece".

> YC: Mind the template.

Ethical issues
--------------
No


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


Review #159B
===========================================================================

Recommendation
--------------
1. Reject

Novelty
-------
3. Incremental improvement

Contribution made by replication/reproduction
---------------------------------------------
1. Not applicable - paper is not for replicability track

Value to the community
----------------------
2. Little value

Reproducibility
---------------
2. Parts can be reproduced

Supplementary material
----------------------
3. All supplementary material

Writing quality
---------------
2. Needs improvement

Reviewer expertise
------------------
3. Knowledgeable

Paper summary
-------------
The paper addresses the problem of double counting tokens in decentralized financial applications. Double counting the tokens in a DeFi protocol could inflate the value of that the protocol.

Reasons to accept
-----------------
- Interesting problem

Reasons to reject
-----------------
- Inadequate background
- Submission seems incomplete

Comments for authors
--------------------
Thanks for submitting your work to IMC!

- [ ] The definition of TVL as “total amount of assets that are currently being used” is confusing. Especially, since you have not yet defined what constitutes a DeFi protocol, readers might not understand what “locking” refers to.

> YC: Explain what consitutes

- [ ] The second paragraph in introduction does not explain what the double counting problem is, and why it happens with TVLs.

- [ ] The introduction is also confusing: The second paragraph makes it seem that the authors are referring to double counting of an asset _within_ a protocol, but towards the end they seem to indicate otherwise.

> YC: Check the intro and second paragraph again.

- [ ] The definitions presented in background are unclear, and assume too much from a reader. In defining a CDP, you introduce the term “stablecoins” but do not define it. Similarly, liquidity pools, DeFi project, and protocol (which has a different meaning in a networking community, especially) are not defined.

> YC: Do we actually need the definitions???

- [ ] There are no citations or pointers to the measurement platforms mentioned in 2.3. Also, why are most of the text in italics?

> YC: Remove italices and add reference to the platforms.

- [ ] The methodology is still unclear: How do you gather details of all transactions, and over what period? The analyses are very basic, and the section looks incomplete.

> YC: Further clarify the data fetching process.

Ethical issues
--------------
No


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


Review #159C
===========================================================================

Recommendation
--------------
1. Reject

Novelty
-------
4. New contribution

Contribution made by replication/reproduction
---------------------------------------------
1. Not applicable - paper is not for replicability track

Value to the community
----------------------
2. Little value

Reproducibility
---------------
2. Parts can be reproduced

Supplementary material
----------------------
2. Some supplementary material

Writing quality
---------------
1. Unacceptable

Reviewer expertise
------------------
2. Some familiarity

Paper summary
-------------
This paper submits that the traditional method of tallying value in the decentralized finance ecosystem involves overestimation due to doubly counting value in derivative tokens. To reduce this effect, the authors propose a new method that considers the total redeemable instead. The study emperically verifies the effect of double counting using the traditional approach and validates the benefits of the proposed metric.

Reasons to accept
-----------------
- Paper does a good job at explaining the problem of double counting

Reasons to reject
-----------------
- There is no related work discussion of any kind. There are two references in the entire paper. These are academic works, but hardly discussed as such. While I want to trust that the proposed method is new and that other works would be adjacent, it'd be nice to see the authors motivate where their work stands compared to others.

- I'm sorry to be so blunt about this, but the overal writing quality and structure of the manuscript is poor.

Comments for authors
--------------------
### REMARKS/SECTION

#### INTRODUCTION

- [ ] "It is not always clear how these platforms calculated the TVL or what biases may be present in the data" => It is not clear to the reviewer how this lack of transparency in calculating the total value locked relates to the double counting problem that the paper tries to solve.

> YC: clarify how platforms calculate TVL and why the methodology is opaque using own words.

- "of the sample DeFi system" => Please be more explicit (immediately). It might be helpful to precede the research questions with a goal statement that makes mention of validation on a selected defi system.

> YC: Be more detailed.

#### BACKGROUND

- [ ] "that allow anyone to generate stablecoins" => You could consider adding a background definition of stablecoins.

> YC: Still the definition problem.

- [ ] "Total Value Locked" => The presentation of TVL here suggests that it might be pretty straightforward to calculate. The reviewer was wondering how this relates to the statement in the intro that TVL oftentimes involves a lack of transparency.

> YC: Add "some platforms are not transparent".

- [X] I think the enumeration of defi protocols could be enriched with citations

> YC: Calculate the TVR of the whole DeFi system.

- [ ] "the sample DeFi system consisting of seven protocols" => How was "the sample" selected or established? Is it representative? What are the alternatives?

> YC: Consider remove these.

#### METHODOLOGY

- [ ] "on ethereum at block 17313217" => Relevance unclear

> YC: Consider remove the snapshot data.

- "We also fetch the token price data from the CoinGecko and Uniswap V2" => Choice unmotivated

> YC: Elaborate on why choosing this data source.

#### DATA ANALYSIS

- [ ] "Figure 3, within the context of the TVR framework, sheds light on the proportions of TVL inflows and outflows, emphasizing the importance of eliminating double counting to obtain a more reliable measure of the actual value accessible within the DeFi ecosystem." => I renew my questions about how the sample was established/select. Are these **the** mainstream defi protocols, or did you leave out others? If the selection were different, what would this do to the analysis and Fig 3, and the estimation of TVR over TVL benefits?

> YC: Consider remove these data.


#### RELATED WORK/REFERENCES

- [X] There is no related work section or discussion. There's two citations in the bib. Where cited in text (both in section 2.1 -- background), these are not exactly discussed.

- [ ] The reviewer is no expert on defi, but a quick search reveals existing literature that seems highly relevant, yet did not make an appearance

> YC: Add these two

[1] Stepanova et al. "Review of Decentralized Finance Applications and Their Total Value Locked" in TEM, 2021
[2] Cumming et al. "Decentralized finance, crypto funds, and value creation in tokenized firms"

#### NITPICKS

- [X] The running title on page 3 linebreaks, which looks odd and might be avoidable with a short \title[short]{long}

- [X] There's unusual extended text in italics in Section 2.3

- [X] Table 1 doesn't look good. The cells linebreak unnecessary and the quantities and amounts appear to flip-flop between left and right alignment. The Table is also way too wide.

- [X] Table 2 seems unnecessary tall

Ethical issues
--------------
No
