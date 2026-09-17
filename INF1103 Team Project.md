# **SITogether**

***1\. Problem Statement and Target Users***

* **Problem Statement:** SIT students have **limited** opportunities to discover and meaningfully interact with new people beyond **face-to-face** encounters, making it **difficult** to form **new social and romantic relationships**.   
* **Background:** Despite being part of a **large student community,** students may only interact with a **small** group of people through their **classes**, **clubs**, or **existing social circles**. As a result, many students may not have the opportunity to meet or get to know others across the **wider SIT community**.   
* **Objective:** To create a programme that provides SIT students with more opportunities to discover, interact with, and get to know **new** people, with the aim of **encouraging meaningful social** and **romantic connections**.   
* **Target Audience:** SIT Students

***2\. User Inputs \- Link to Google Sheets***  
**Background Information:**

* Name, Birthday (DD/MM/YYYY) → Zodiac & Ba Zi, Religion, MBTI → 16 Personalities  
* Year, Course, Student ID

**Personal Information:**

* Sexual Orientation: Heterosexual/ Homosexual/ Bisexual   
* Here For: Friends/ Relationship  
* Expectations in Relationships 

**Extracurriculars:** 

* Current CCAs/ Events Joined (in SIT), Hobbies,Outside Interest Group 


***3\. Use of AI \- Claude***

| AI Feature | How AI is Utilized | AI Output/Recommendation |
| :---- | :---- | :---- |
| **Compatibility Matching** | AI will analyse user’s profiles, to identify similarities between two students. | Generates a ***Compatibility Score*** and highlights key areas of similarity. |
| **Personalised Match Recommendations** | AI analyses a user’s profile together with profiles they liked or skipped, to better understand their preferences over time. | Recommends students who are more likely to be compatible with a user and improves on future matchmaking suggestions. |
| **Conversations & Date Suggestions** | AI uses information from both matched user’s profiles and shared interests to generate personalised suggestions. | Provides both users with:  Conversation Starters Common-Interest Topics Possible Date Activities Relevant SIT Events |
| **Content Safety & Moderation** | AI analyses messages and profile content for potentially inappropriate behavior. | Flags potentially harmful content for review and warns users where appropriate. Repeated or serious violations are escalated. |
| **Profile Image Verification** | AI analyses uploaded profile images for signs of manipulated, AI-generated or duplicated images. | Assigns a risk/verification result and flags suspicious images for further review rather than automatically banning the student. |
| **Match Feedback & Compatibility Analytics** | AI analyses feedback after matches, such as whether users continued chatting or mutually liked each other. | Identifies patterns associated with successful matches and uses them to improve future compatibility recommendations. |

***4\. Business Rules***

| SIT Student Validation | Only verified SIT students may create an account. Users must register using their SIT student email / Student ID. |
| :---- | :---- |
| **Account/Profile Eligibility** | A user must have a **verified account and completed profile** before appearing in matchmaking recommendations. |
| **Compatibility Range** | Matches will be according to the AI-generated compatibility score:  **85 \- 100%**: High Compatibility **70 \- 84%**: Shown after high compatibility users **Below 70%**: Low Compatibility; Lower Priority  |
| **Match Status**  | **“Accept", “Reject”:** Social media handles will be revealed once a match is created. |
| **Flag System *(Human-In-The- Loop System)***  | AI will assign potentially inappropriate or suspicious content a **risk/confidence score**. Low-confidence cases will not automatically penalise users. Content that exceeds a defined threshold will be **flagged for human review** before disciplinary action is taken.  |
| **Violation System** | Violations will be recorded against the user's account: **1st Violation:** In-App Warning **2nd Violation:** Email Warning **3rd Violation:** Escalate to Administrator |
| **Match Recommendation Rule** | Users who have already **rejected, blocked, or reported each other** will not be recommended to one another again. Existing matches should also be excluded from new recommendations.  |
| **Blocking & Reporting Rule** | When a user blocks another user, both users will be removed from each other's recommendations. Reports will be stored for administrator review.  |

