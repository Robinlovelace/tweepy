# BigLoad.R - for loading large amounts of twitter data into R
library(rgdal)
library(maptools)
library(rjson) # library used to load .json files

# Set parameters:
json_loc <- "/scratch/tweepy/data/unzipped/" # where are the raw .json files stored? (json location)
csv_des <- "/scratch/tweepy/data/unzipped/tdf/" # where will the .csv files go? (must exist)
text_string <- "letour|tourdefrance|tdf|tour de"
# only save messages that include this string # omitted by default "" means all tweets, | means or
bounds <- readOGR("/scratch/tweepy/Carnival/", "geosel") # load the polygons that will filter the tweets
proj4string(bounds) <- CRS("+init=epsg:4326")
nlines <- final_output <- NULL
old <- setwd(json_loc) # the directory of files you want to load

# Unzip the files saved by tweepy (see https://github.com/Robinlovelace/tweepy)
# skip this stage if they are already unzipped

# If the files are too large, they may need splitting up:

# x <- list.files(pattern = "json") 
# i <- x[1]
# start_time <- Sys.time()
# for(i in x){
#   mess <- paste0("split -l 100000 ", i, " split-", i) # chunks of 1 million
#   system(mess)
#   print(x[i])
# }
# (split_time <- Sys.time() - start_time)

# Save to "unzipped" (e.g. with gunzip), load these files
files <- list.files(pattern = "split") # only select files that have been split
# i <- files[1] # uncomment to load 1
start_time <- Sys.time()

# The per file for loop
# for(i in files[1:2]){ # test loop
for(i in files){
# tweets <- fromJSON(sprintf("[%s]", paste(readLines(i, n=1000), collapse=","))) # test subset
  tryCatch({
    tweets <- fromJSON(sprintf("[%s]", paste(readLines(i), collapse=","))) # full dataset
  }, error=function(e){paste0("Error ", which(i == files))})
  
coords <- sapply(tweets, function(x) x$coordinates$coordinates )
nuls <- sapply(coords, function(x) is.null(x)) # identify out the problematic NULL values
coords[nuls] <- lapply(coords[nuls], function(x) x <- c(0, 0)) # convert to zeros to keep with unlist
coords <- matrix(unlist(coords, recursive = T), ncol = 2, byrow = T)
text <- as.character(sapply(tweets, function(x) x$text ))
created <- sapply(tweets, function(x) x$created_at)
tweet_id <- sapply(tweets, function(x) x$id_str)
created <- strptime(created, "%a %b %d %H:%M:%S +0000 %Y")
language <- sapply(tweets, function(x) x$lang )
n_followers <- sapply(tweets, function(x) x$lang )
user_created <- sapply(tweets, function(x) x$user$created_at)
n_tweets <- sapply(tweets, function(x) x$user$statuses_count)
n_followers <- sapply(tweets, function(x) x$user$followers_count)
n_following <- sapply(tweets, function(x) x$user$friends_count)
user_location <- sapply(tweets, function(x) x$user$location)
user_description <- sapply(tweets, function(x) x$user$description)
user_id <- sapply(tweets, function(x) x$user$id)
user_idstr <- sapply(tweets, function(x) x$user$id_str)
user_name <- sapply(tweets, function(x) x$user$name)
user_screen_name <- sapply(tweets, function(x) x$user$screen_name)
lang <- sapply(tweets, function(x) x$lang )
# n_retweets <- sapply(tweets, function(x) x$retweet_count) # not working

t_out <- data.frame(text, lat = coords[,2], lon = coords[,1], created, tweet_id,
  language, n_followers, user_created, n_tweets, n_followers, n_following,
  user_location, lang)

sel <- grepl(text_string, t_out$text, ignore.case = T ) # text filter 

# # Geo part
# geoT <- SpatialPointsDataFrame(coords= matrix(c(t_out$lon, t_out$lat), ncol=2), data=t_out)
# proj4string(geoT) <- CRS("+init=epsg:4326")
# geosel <- geoT[bounds, ]
# tsel <- geoT[0, ] # geoT[sel, ] # use sel to include geo tweets
# output <- spRbind(geosel, tsel) # remove if only geosel is of interest
t_out$filenum <- which(files == i)
output <- t_out[sel, ] # if uninterested in spatial data


print(paste0(which(files == i) / length(files) * 100, "% done"))
nlines <- nlines + nrow(t_out)

t_out$filenum <- which(files == i)
# write.csv(output, file = paste0(csv_des, which(files == i),".csv")) # may need output@data
final_output <- rbind(final_output, output)
print(paste0(which(files == i) / length(files) * 100, "% done"))
}
end_time <- Sys.time()
(time_taken <- end_time - start_time) 





# # read the files back in! only if csvs saved separately
# outs <- list.files(path = csv_des, pattern=".csv", full.names=T)
# output <- read.csv(outs[1])
# for(j in outs[-1]){
#   tryCatch({
#   output <- rbind(output, read.csv(j))
#   }, error=function(e){paste0("Error ", which(outs == j))})
#   num <- which(outs == j)
# }
# summary(output)
# write.csv(output, "output-letour.csv")
# setwd(old)
