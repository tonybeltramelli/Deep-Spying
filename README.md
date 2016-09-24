# Deep-Spying
*Spying using Smartwatch and Deep Learning*

[![License](http://img.shields.io/badge/license-APACHE2-blue.svg)](LICENSE.txt)

<img src="logo.png?raw=true" align="right"/>

This repository contains the code implemented for my Master's thesis project submitted in fulfillment of the requirements for the degree of Master of Science at the [IT University of Copenhagen](http://en.itu.dk/) supervised by [Professor Sebastian Risi](http://sebastianrisi.com/).

* A video demo of the system can be seen [here](https://youtu.be/ZBwSfvnoq5U)
* The paper is available at [http://arxiv.org/abs/1512.05616](http://arxiv.org/abs/1512.05616)

The following software is shared for educational purpose only. The author of the code and its affiliated institution are not responsible in any manner whatsoever for any damages, including any direct, indirect, special, incidental, or consequential damages of any character arising as a result of the use or inability to use this software. Neither the names of the author or the name of its affiliated institution may be used to endorse or promote products derived from this software. Please find more details in the provided Licence file.

## Abstract
Wearable technologies are today on the rise, becoming more common and broadly available to mainstream users. In fact, wristband and armband devices such as smartwatches and fitness trackers already took an important place in the consumer electronics market and are becoming ubiquitous. By their very nature of being wearable, these devices, however, provide a new pervasive attack surface threatening users privacy, among others.

In the meantime, advances in machine learning are providing unprecedented possibilities to process complex data efficiently. Allowing patterns to emerge from high dimensional unavoidably noisy data.

The goal of this work is to raise awareness about the potential risks related to motion sensors built-in wearable devices and to demonstrate abuse opportunities leveraged by advanced neural network architectures.

The LSTM-based implementation presented in this research can perform touchlogging and keylogging on 12-keys keypads with above-average accuracy even when confronted with raw unprocessed data. Thus demonstrating that deep neural networks are capable of making keystroke inference attacks based on motion sensors easier to achieve by removing the need for non-trivial pre-processing pipelines and carefully engineered feature extraction strategies. Our results suggest that the complete technological ecosystem of a user can be compromised when a wearable wristband device is worn.

### Keywords
Security, Side-Channel Attack, Keystroke Inference, Motion Sensors, Deep Learning, Recurrent Neural Network, Wearable Computing

## International media coverage
* [Wired UK](http://www.wired.co.uk/news/archive/2015-12/21/smartwatch-typing-spying)
* [GEEK](http://www.geek.com/news/your-smartwatch-can-guess-your-pin-1642965/)
* [El Pais](http://tecnologia.elpais.com/tecnologia/2015/12/21/actualidad/1450722128_471371.html)
* [Vice](http://motherboard.vice.com/read/heres-how-your-smartphone-can-reveal-what-youre-typing)
* [Gizmodo](http://gizmodo.com/your-smartwatchs-motion-sensors-can-reveal-everything-y-1750442236)
* [Lifehacker Australia](http://www.lifehacker.com.au/2016/01/should-you-be-worried-about-smartwatches-and-smartphones-spying-on-you/)
* [Huffington Post](http://www.huffingtonpost.com/entry/smartwatch-hack-passwords_5689e6d5e4b014efe0daceeb)
* [IFL Science](http://www.iflscience.com/technology/new-ways-your-smartwatch-and-phone-may-be-spying-you-how-worried-should-you-be)
* [XDA Developers](http://www.xda-developers.com/xda-external-link/how-your-smartwatch-can-reveal-what-youre-typing/)
* [Naked Security](https://nakedsecurity.sophos.com/2016/01/11/could-your-smartwatch-be-giving-away-your-atm-pin/)
* [Softpedia](http://news.softpedia.com/news/smartwatches-can-be-used-to-spy-on-your-card-s-pin-code-498756.shtml)
* [Version2](http://www.version2.dk/artikel/itu-studerende-sensorer-i-smartwatch-kan-afsloere-pinkoden-til-dit-dankort-549635)
* [Forbes](http://www.forbes.com/sites/kalevleetaru/2016/01/15/when-cameras-and-wearables-could-be-used-to-steal-passwords-and-keys/)
* [phys.org](http://phys.org/news/2016-01-ways-smartwatch-spying.html)

On Danish national TV channel [TV2 NewScience](http://play.tv2.dk/programmer/magasiner/serier/newscience/smarture-kan-afsloere-din-pinkode-109753/)  
University blog post [here](http://en.itu.dk/About-ITU/Press/News-from-ITU/Your-smartwatch-can-reveal-your-PIN-code)  
Read comments on [Hacker News](https://news.ycombinator.com/item?id=10758298)

## Citation

    @article{beltramelli2015deep,
      title={Deep-Spying: Spying using Smartwatch and Deep Learning},
      author={Beltramelli, Tony and Risi, Sebastian},
      journal={arXiv preprint arXiv:1512.05616},
      year={2015}
    }

## Fun fact
The original project name was "SWAT: Spying using Wearable Wristband/Armband Technology", which explains why some packages still reflect this old name.
