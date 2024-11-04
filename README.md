# KineticFluxProfilingProject
## 	1. simulation for k_app in the linear pathway
To get accurate estimation, we simulated the labeling fraction with different values of _r_ ($k_x/k_y$), and fit single exponential to obtain _k<sub>Y_app</sub>_. In this code, we compared the fitted _k<sub>app</sub>_ with the curve of the equation $k_{app}=k_X*k_Y/(k_X+k_Y)$, and the result shows that they are very similar.

![simulation for k_app in the linear pathway](https://github.com/user-attachments/assets/90dc7f4d-0de3-4b1f-a75f-ade4b9b3e735)

## 	2. k_adj fitting
Fitting _Y<sub>L</sub>_ will yield _k<sub>Y_app</sub>_ (the apparent rate constant) rather than _k<sub>y</sub>_ (the actual rate constant) because _Y<sub>L</sub>_ is subject to a delay caused by the upstream reaction. To minimize this impact and obtain a more accurate value of _k<sub>y</sub>_, we adopt this code to adjust it.

![image](https://github.com/user-attachments/assets/18582d8c-fe38-4d99-ba0e-d8361b004b3b)

Taking Pyr and Cit as an example here, we regard Cit as the direct downstream of Pyr. After entering the labeling fraction data of both into _k_value_fitting.csv_ and running the code, we can obtain the adjustment results below.

![image](https://github.com/user-attachments/assets/44b70163-8c66-4fed-bb87-4e868da44ac2)

Here _k_um_ is the k value of upstream metabolite; _k_dm_ori_ is the original k_value of downstream metabolite; _k_dm_adj_ is the k_value of downstream metabolite after adjustment.
