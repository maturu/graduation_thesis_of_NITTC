<p>
  <a href="https://www.ipsj.or.jp/"><img src="https://img.shields.io/badge/Soiety-IPSJ-blue.svg"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Code-Python3.6-yellow.svg"></a>
  <a href="https://github.com/maturu/graduation_thesis_of_NITTC/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <a href="https://github.com/maturu/graduation_thesis_of_NITTC/issues"><img src="https://img.shields.io/badge/Issues-error-red.svg"></a>
</p>

[Paper submitted to The 81st National Convention of IPSJ](https://ipsj.ixsq.nii.ac.jp/ej/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=197335&item_no=1&page_id=13&block_id=8)

# Graduation thesis of NITTC: Automatic Detection System of Plagiarized Reports Based on Retrieval of Website
## Introduction
 In recent years, because of the rapid development of internet, many universities, vocational school's students submit dishonest reports that are plagiarized from website as their homework to teacher. Such behavior makes it difficult to accurately evaluate grades for them, and potentially causes the problem of copyright infringement. Manual detection of such reports is time consuming so that it becomes heavy burden of teachers.

 In order to solve this problem, in this research the author propose a system to automatic detect plagiarism of student's report from the website.  It not only distinguishes dishonest reports for teachers but also identifies the detailed plagiarized part via the comparison of websites. Proposed system has three modules: 1) extraction of feature words of each report, 2) searching of candidate plagiarized websites via search engine, 3) comparison of reports and such websites.

 In evaluation of the sufficiency of proposed system, the author conduct a simulation experiment in which 10 plagiarized reports and 10 none-plagiarized reports are used. As the results, 7 of 10 plagiarized reports are successfully reported as plagiarized ones. On the other hand, all none- plagiarized reports have low possibilities of plagiarism. In future, the author plan to further introduce the combination of feature words in web searching, and parallel process of detection.

## Overview of the proposed system
<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/15319238/77822078-ca074900-7132-11ea-80a6-e8a34928cd0b.png" ><br>
  <label>Figure 1: System Overview</label>
</p>

Figure 1 shows a schematic diagram of the proposed system. 

First, the teacher selects and inputs appropriate words from the report tasks. 

Second, the proposed system calculates the TF-IDF weights of the words included in each report, and extracts the top three words as the characteristic words of the report based on the TF-IDF weights. A Web search is performed as a search term, and the top k results of the search result are acquired as the plagiarism source candidate Web site. 

Third, the k sentences of each acquired Web site and the text of the report are compared to detect plagiarism, using the Smith-Waterman algorithm to detect similar subsequences from two character sequences.

Finally, the ratio of the plagiarized portion to the report is calculated as the plagiarism rate, and if this value exceeds the set threshold, the report is regarded as plagiarized.

## References
1. ![村上寛明，堀田圭佑，肥後芳樹，井垣宏，楠本真 二:Smith-waterman アルゴリズムを利用したギャップ を含むコードクローン検出，情報処理学会論文誌， Vol.55，No.2，pp.981–993 (2014).](https://ipsj.ixsq.nii.ac.jp/ej/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=98517&item_no=1&page_id=13&block_id=8)

2. ![上野修司，高橋勇，黒岩丈介，白井治彦，小高知宏， 小倉久和:複数の Web ページから剽窃したレポートの 発見支援システムの実装，情報処理学会研究報告コン ピュータと教育 (CE)，Vol.2006，No.130 (2006-CE- 087)，pp.41–46 (2006).](https://ipsj.ixsq.nii.ac.jp/ej/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=54157&item_no=1&page_id=13&block_id=8)

3. ![森祐貴，谷川佳延，吉田博哉:引用個所を考慮した 剽窃レポートの検出システムの開発，2015 年度 情 報処理学会関西支部 支部大会 講演論文集，Vol.2015 (2015).](https://ipsj.ixsq.nii.ac.jp/ej/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=145700&item_no=1&page_id=13&block_id=8)
