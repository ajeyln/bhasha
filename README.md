<h1 align="Center"> BHASHA - a language learning app</h1>

## Table of Content

* [Background](#back)
* [Ideas/Features](#features)
* [Execution](#exec)
* [Useful Links](#useful)
* [Contributions](#contributions)


## <a name="back"></a> Background

"Bhasha" means Language in Sanskrit.

This repository contains source code, presentation decks and images related Bhasha learning application.

For learning any language, we may need to memorize words to improve our vocabulary. Bhasha attempts to help you address this problem. 

Source Language is a language that user wants to learn. And Destination Language(s) are languages, which a user employs to understand Source Language.

In our examples, Source Language is German and Destination Languages are English or any Indian Language. One can use any google supported language family.

Recent studies (Figure 1) show that german has been trending language now for learning amongst foreigners. Having limited resources for learning, Bhasha aims to help these students. 


![Figure 1 Foreigners learning German source : Deutsch als Fremdsprache weltweit 2020, [Datenerhebung 2020](media_sources\deutsch-als-fremdsprache-data.pdf) ](./images/german_stats.png)<br />

Figure 1 Foreigners learning German source : Deutsch als Fremdsprache weltweit 2020, [Datenerhebung 2020](media_sources\deutsch-als-fremdsprache-data.pdf)

## <a name="features"></a> Features

Bhasha offers following features

* support for custom words list 
* web game interface for learning Source to Destination languages and vice versa 
* audio support (native speaker) 
* open source development

## <a name="exec"></a> Execution

Bhasha is series of python scripts employed for users to help with language learning. We have used HTML/JS based frontend, and GOOGLE SDK for preparing language content. 


Please use python version 3.9 or above

and install following Python modules :

```
googletrans        4.0.0rc1
gTTS               2.2.4
```
And for advanced details on execution, please refer to [README](app/README.md)


## <a name="useful"></a> Useful Links
| **Sl. No.** | **Link** | **Remarks** |
----------|--------------|--------------
1| [GOOGLE Translate package](https://pypi.org/project/googletrans/)| translation package for py |
2| [GOOGLE supported language ](https://cloud.google.com/translate/docs/languages)|  |


## <a name="contribution"></a> Conrtbutions
1 Concept, Design & Development, and Presentation [Vasudeva Nayak Kukkundoor](https://www.linkedin.com/in/vasudeva-nayak-kukkundoor-04183816/) 

2 Devlopment, and Testing [Ajeya Nayak](https://www.linkedin.com/in/ajeya-nayak-34801766/)

3 Frontend design and code [CodingNepal](https://www.codingnepalweb.com/)