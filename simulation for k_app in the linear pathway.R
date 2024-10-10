library(dplyr)
library(ggplot2)
library(egg)

# scenario 2
t = 0.01*(1:1000)
k_Y = 0.5
RSD = 0.2 # relative standard error of isotope fraction
frac.sim = list()
r <- c(0.01,0.03,0.1,0.3,1.1,3,10,30,100) # k_X = r*k_Y
for (i in 1:length(r)) {
  k_X = r[i]*k_Y
  f = 1 + 1/(r[i]-1)*exp(-k_X * t) - r[i]/(r[i]-1)*exp(-k_Y*t) +rnorm(1000, mean = 0, sd = RSD)
  frac.sim[[i]] <- data.frame(time = t, fraction = f,ratio = r[i])
}

frac.sim <- as.data.frame(do.call(rbind, frac.sim))

k.fit = data.frame(ratio = r, k = NA, k.e = NA)

for (i in 1:length(r)) {
  df <- frac.sim %>% filter(ratio == r[i])
  model <- nls(fraction ~ (1 - exp(-k * time)), data = df, start = list(k = 0.5))
  result <- summary(model)
  k.fit$k[i] = result$coefficients[1,1]
  k.fit$k.e[i] = result$coefficients[1,2]
}

ggplot(k.fit, aes(x = r, y = k/k_Y, ymin = (k-k.e)/k_Y,ymax = (k+k.e)/k_Y)) +
  geom_point() +geom_errorbar(width = 0.1)+scale_x_log10()+scale_y_log10()+
  geom_abline(slope = 1, intercept = 0, color = 'red')+
  geom_abline(slope = 0, intercept = 0, color = 'red')+
  geom_line(aes(x = r, y = r/(r+1)), color = 'blue')+
  geom_text(label = 'k_app = k_X*k_Y/\n(k_X+k_Y)',aes(x = 5, y = 0.2), color = 'blue', size = 8)+
  geom_text(label = 'k_app = k_X',aes(x = 0.03, y = 0.06), color = 'red', size = 8, angle = 49)+
  geom_text(label = 'k_app = k_Y',aes(x = 0.05, y = 0.7), color = 'red', size = 8)+
  egg::theme_presentation()+
  xlab('r = k_X / k_Y') + ylab('k_app / k_Y')

