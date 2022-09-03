# Dockerfile
FROM tomcat:<specify-a-version>
MAINTAINER swipejobs <devops@swipejobs.com>

WORKDIR "/usr/local/tomcat/"
# War file replacement
RUN rm -rf webapps/*
COPY hello-world.war webapps/ROOT.war

RUN groupadd --gid 1000 catalina \
         && useradd --uid 1000 --gid catalina --shell /bin/bash --create-home catalina
USER catalina

EXPOSE 8080
ENV JAVA_OPTS="-Xmx12g-Xms12g"

ENTRYPOINT ["bin/catalina.sh", "run"]



# multistage build
# FROM maven AS build
# WORKDIR /app
# COPY . .
# RUN mvn package

# FROM tomcat
# COPY --from=build /app/target/hello-world.war /usr/local/tomcat/webapps/ROOT.war