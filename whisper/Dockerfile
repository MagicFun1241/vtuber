FROM ubuntu:22.04 AS build
WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential cmake git && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ggml-org/whisper.cpp.git .
RUN cmake -B build \
    -DGGML_AVX=OFF \
    -DGGML_AVX2=OFF \
    -DGGML_FMA=OFF \
    -DGGML_F16C=OFF \
    -DGGML_NATIVE=OFF \
    -DGGML_CUDA=OFF \
    -DGGML_VULKAN=OFF \
    -DGGML_METAL=OFF && \
    cmake --build build --config Release -j$(nproc)

FROM ubuntu:22.04
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl wget libgomp1 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /app/build/bin/ /usr/local/bin/
COPY --from=build /app/build/src/*.so* /usr/local/lib/
COPY --from=build /app/build/ggml/src/*.so* /usr/local/lib/
ENV LD_LIBRARY_PATH=/usr/local/lib
