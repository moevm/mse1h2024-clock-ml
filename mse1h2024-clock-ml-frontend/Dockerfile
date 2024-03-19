FROM node:latest

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm install -g serve@14.2.1

COPY . .

RUN npm run build

EXPOSE 80

CMD ["npx", "serve", "-s", "dist", "-l", "80"]
