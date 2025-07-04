FROM node:16

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép package.json và cài đặt dependencies
COPY package.json package-lock.json ./
RUN npm install

# Sao chép code vào container
COPY . .

# Build ứng dụng React
RUN npm run build

# Cài đặt server để phục vụ build
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Chạy ứng dụng
CMD ["serve", "-s", "build", "-l", "3000"]