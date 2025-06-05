FROM node:18

WORKDIR /app

<<<<<<< HEAD
ENV CHOKIDAR_USEPOLLING=true
ENV NODE_ENV=development

=======
>>>>>>> origin/master
COPY package.json package-lock.json ./
RUN npm install

COPY . .
<<<<<<< HEAD
EXPOSE 3000 24678
CMD ["npm", "run", "dev", "--", "--turbo"]
=======
EXPOSE 3000
CMD ["npm", "run", "dev"]
>>>>>>> origin/master
