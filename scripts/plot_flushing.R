library(tidyverse)
library(ggplot2)
library(stringr)

# three directories
dirs <- c("../sims/modern",
         "../sims/coarse",
         "../sims/v_coarse")
names <- c("High", "Med", "Low")

regexp <- "[[:digit:]]+"
all_data <- data.frame(matrix(ncol=4,nrow=0))
x<-c("Time", "Particles", "Model", "Release")
colnames(all_data) <- x

# in directory
i <- 1
for (dir in dirs) {

    csv_files <- list.files(dir, pattern="^particles_.*.csv")
    # for each csv file with pattern
    for (csv_file in csv_files) {

        release_time <- str_extract(csv_file, regexp)
        # load and add to main data frame
        temp_df <- read.csv(paste0(dir,"/",csv_file))
        temp_df <- temp_df %>% mutate(Model = names[i])
        temp_df <- temp_df %>% mutate(Release = release_time)

        all_data <- rbind(all_data, temp_df)
    }
    i <- i + 1
}

all_data$Time <- all_data$Time * 240.0 / 60.0 / 60.

# calculate mean for each dir/Time
mean_model <- all_data %>% group_by(Model,Time) %>% summarise(Particles=mean(Particles), Release="Mean")

# plot
p <- ggplot() + 
     geom_line(data=all_data, alpha=0.2, aes(x=Time, y=Particles, group=interaction(Release, Model), color=Model)) +
     geom_line(data=mean_model, aes(x=Time, y=Particles, group=interaction(Release, Model), color=Model)) +
     scale_color_brewer(palette="Set1")+theme_minimal(base_size = 18) +
     scale_color_discrete(breaks=c('High', 'Med', 'Low')) +
     labs(x="Time since release (hrs)")

ggsave(filename="Lagoon_flushing_rate.pdf", p, width=297, height=210, units="mm")
