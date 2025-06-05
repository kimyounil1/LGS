FROM node:18

WORKDIR /app

ENV CHOKIDAR_USEPOLLING=true
ENV NODE_ENV=development

COPY package.json package-lock.json ./
RUN npm install

COPY . .
EXPOSE 3000 24678
CMD ["npm", "run", "dev", "--", "--turbo"]
