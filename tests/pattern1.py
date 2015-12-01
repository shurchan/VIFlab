#!/usr/bin/python
# -*- coding: utf-8 -*-

from pattern.vector import Document

s = '''
Management’s Discussion and Analysis of Financial Condition and Results of Operations  This
section and other parts of this Annual Report on Form 10-K (“Form 10-K”) contain forward-looking statements, within the
meaning of the Private Securities Litigation Reform Act of 1995, that involve risks and uncertainties. Forward-looking statements provide current expectations of future events based on certain assumptions and include any statement that does not
directly relate to any historical or current fact. Forward-looking statements can also be identified by words such as “future,” “anticipates,” “believes,” “estimates,” “expects,” “intends,”
“plans,” “predicts,” “will,” “would,” “could,” “can,” “may,” and similar terms. Forward-looking statements are not guarantees of future performance and the Company’s actual
results may differ significantly from the results discussed in the forward-looking statements. Factors that might cause such differences include, but are not limited to, those discussed in Part I, Item 1A
of this Form 10-K under the heading “Risk Factors,” which are incorporated herein by reference. The following discussion should be read in conjunction with the consolidated financial statements and notes thereto included in Part II,
Item 8 of this Form 10-K. All information presented herein is based on the Company’s fiscal calendar. Unless otherwise stated, references to particular years, quarters, months or periods refer to the
Company’s fiscal years ended in September and the associated quarters, months and periods of those fiscal years. Each of the terms the “Company” and “Apple” as used herein refers collectively to Apple Inc. and its
wholly-owned subsidiaries, unless otherwise stated. The Company assumes no obligation to revise or update any forward-looking statements for any reason, except as required by law.
Overview and Highlights  The Company designs, manufactures and
markets mobile communication and media devices, personal computers and portable digital music players, and sells a variety of related software, services, accessories, networking solutions and third-party digital content and applications. The Company
sells its products worldwide through its retail stores, online stores and direct sales force, as well as through third-party cellular network carriers, wholesalers, retailers and value-added resellers. In addition, the Company sells a variety of
third-party Apple compatible products, including application software and various accessories through its online and retail stores. The Company sells to consumers, small and mid-sized businesses and education, enterprise and government customers.
 Fiscal 2015 Highlights  Net sales rose 28% or $50.9
billion during 2015 compared to 2014, driven by a 52% year-over-year increase in iPhone® net sales. iPhone net sales and unit sales in 2015 increased in all of the Company’s reportable
operating segments. The Company also experienced year-over-year net sales increases in Mac®, Services and Other Products. Apple Watch®,
which launched during the third quarter of 2015, accounted for more than 100% of the year-over-year growth in net sales of Other Products. Net sales growth during 2015 was partially offset by the effect of weakness in most foreign currencies
relative to the U.S. dollar and lower iPad® net sales. Total net sales increased in each of the Company’s reportable operating segments, with particularly strong growth in Greater China
where year-over-year net sales increased 84%.  In April 2015, the Company announced a significant increase to its capital return program by raising
the expected total size of the program to $200 billion through March 2017. This included increasing its share repurchase authorization to $140 billion and raising its quarterly dividend to $0.52 per share beginning in May 2015. During 2015, the
Company spent $36.0 billion to repurchase shares of its common stock and paid dividends and dividend equivalents of $11.6 billion. Additionally, the Company issued $14.5 billion of U.S. dollar-denominated,
€4.8 billion of euro-denominated, SFr1.3 billion of Swiss franc-denominated, £1.3 billion of British pound-denominated, A$2.3 billion of Australian dollar-denominated and ¥250.0 billion
of Japanese yen-denominated term debt during 2015.  Fiscal 2014 Highlights
Net sales rose 7% or $11.9 billion during 2014 compared to 2013. This was driven by increases in net sales of iPhone, Mac and Services. Net sales and unit
sales increased for iPhone primarily due to the successful introduction of iPhone 5s and 5c in the latter half of calendar year 2013, the successful launch of iPhone 6 and 6 Plus beginning in the fourth quarter of 2014, and expanded distribution.
Mac net sales and unit sales increased primarily due to strong demand for MacBook Air® and MacBook Pro® which were updated in 2014 with
faster processors and offered at lower prices. Net sales of Services grew primarily due to increased revenue from sales through the App Store®, AppleCare® and licensing. Growth in these areas was partially offset by the year-over-year decline in net sales for iPad due to lower unit sales in many markets, and a decline in net sales of Other
Products. All of the Company’s operating segments other than the Rest of Asia Pacific segment experienced increased net sales in 2014, with growth being strongest in the Greater China and Japan operating segments.
During 2014, the Company completed various business acquisitions, including the acquisitions of Beats Music, LLC, which offers a subscription streaming
music service, and Beats Electronics, LLC, which makes Beats® headphones, speakers and audio software.
  Apple Inc. | 2015 Form 10-K | 23



Table of Contents
In April 2014, the Company increased its share repurchase authorization to $90 billion and the quarterly
dividend was raised to $0.47 per common share, resulting in an overall increase in its capital return program from $100 billion to over $130 billion. During 2014, the Company utilized $45 billion to repurchase its common stock and paid dividends and
dividend equivalents of $11.1 billion. The Company also issued $12.0 billion of long-term debt during 2014, with varying maturities through 2044, and launched a commercial paper program, with $6.3 billion outstanding as of September 27, 2014.
 Sales Data  The following table shows net sales by
operating segment and net sales and unit sales by product during 2015, 2014 and 2013 (dollars in millions and units in thousands):   

'''

d = Document(s, threshold=1)
print d.keywords(top=6)
print d.vector
