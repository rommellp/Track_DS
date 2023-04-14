# Track_DS
Here is a breakdown of the three main events used in this project.

In this Project, I aim to answer three questions about high school track athletes. I want to know:
1.	Has there been growth in the track population?
2.	Is there a performance increase for the years analyzed?
3.	How do performances correlate to the grade level?

The dataset used contains years 1996-2010. This would be a long enough timespan to measure changes, 
but initial processing revealed a lack of data for most years. The years 2004-2007 has the most consistent counts, 
therefor these are the years used. This is true for each events analyzed: the 400m, 800m, and 1500m.

![400m_pop](https://user-images.githubusercontent.com/77018498/232095056-ebdc29e6-21d9-4cc1-8439-e84fa7c9d326.png)
![800m_pop](https://user-images.githubusercontent.com/77018498/232095096-d7b9e425-439e-4436-83aa-7c0f05e87b28.png)
![1500_pop](https://user-images.githubusercontent.com/77018498/232095197-707af1ae-086b-4e13-8de3-94adef5c1ee3.png)

As seen in the figures above, data is consistently missing across the three events. In the 2006 Outdoor Season, 
the 9th grade runners are not well represented. In the 2007 Outdoor Season, both 9th graders and 10th graders are not well represented. 
Still, these years provide the most data.

Taking a look at population for each event, we can see a jump in runners between 2004 and 2005, but a decrease from 2005 to 2007. 
This decrease is likely due to the missing data in 2006 and 2007. With a complete picture of the data, there would likely be a more consistent trend. 
This exact trend is duplicated in the 800m and 400m datasets. 

![400m_part](https://user-images.githubusercontent.com/77018498/232095405-8a347b3e-47d8-4c1f-a19b-08e23019e233.png)
![800m_part](https://user-images.githubusercontent.com/77018498/232095428-943ab1ac-bec7-4f26-ab03-8ebe90bf4bde.png)
![1500_part](https://user-images.githubusercontent.com/77018498/232095447-ae8a9316-8195-4516-ae2f-41b976bf48aa.png)


When looking at the performance, we see trends across these events. By looking at the grade level through time, we notice that 12th graders 
have an average time that slightly drops in the 1500m and 800m, but stays consistent in the 400m. 11th grade runners shed a bit of time also, 
following the same trend as the senior. 10th grade runners seem to be following along, until the final season. This change is likely due to 
the drop in recorded participants in 2007 which skews the average times. 9th grade runners seem to follow along in 2004 and 2005, then have 
abrupt changes in both 2006 and 2007. This is likely due to the lack of recorded participants in both the 2006 and 2007 seasons. This skews 
the average, and misrepresents the average time for these runners.

![400m_grade_perf](https://user-images.githubusercontent.com/77018498/232095601-58e9af24-f2cd-4405-ac8f-688e0cfff228.png)
![800m_grade_perf](https://user-images.githubusercontent.com/77018498/232095610-6a3467cc-ed96-48fe-b635-5c30aad1f0d2.png)
![1500_grade_perf](https://user-images.githubusercontent.com/77018498/232095623-cc0448f9-989d-498a-baf4-e459aa259b63.png)


Lastly, we are looking at the same data, but now with respect to grade level. By shifting the format of the data, we are able to see 
correlations between the performances and the grade level. From this data, we expect to see a drop in average times as runners make 
their way through high school. This is expected because, runners will likely be stronger and more mature by the time they are in their 
final year of high school. In the 1500m, there is only one participant (who is pretty fast) in 9th grade, thus the result is skewed. 
Overall, there seem to be a common trend that shows performances increase as by grade level. 

![400m_perf](https://user-images.githubusercontent.com/77018498/232095749-3e06212c-070d-464b-b606-056ef57d78e7.png)
![800m_perf](https://user-images.githubusercontent.com/77018498/232095771-498360af-2d04-49a7-83a7-8165a73dfcd6.png)
![1500_perf](https://user-images.githubusercontent.com/77018498/232095884-5803601b-3412-48ac-a9f2-fbeba4769698.png)



