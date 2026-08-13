#include <cstdio>
#include <stdexcept>
#include <string>

class FileHandle {
public:
    explicit FileHandle(const std::string& path, const char* mode) {
        fp_ = std::fopen(path.c_str(), mode);
        if (!fp_) {
            throw std::runtime_error("failed to open file");
        }
    }

    ~FileHandle() noexcept {
        if (fp_) {
            std::fclose(fp_);
            fp_ = nullptr;
        }
    }

    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    FileHandle(FileHandle&& other) noexcept : fp_(other.fp_) {
        other.fp_ = nullptr;
    }

    FileHandle& operator=(FileHandle&& other) noexcept {
        if (this == &other) {
            return *this;
        }
        if (fp_) {
            std::fclose(fp_);
        }
        fp_ = other.fp_;
        other.fp_ = nullptr;
        return *this;
    }

    std::string read_all() {
        if (!fp_) {
            throw std::runtime_error("invalid file handle");
        }

        if (std::fseek(fp_, 0, SEEK_END) != 0) {
            throw std::runtime_error("fseek end failed");
        }
        long size = std::ftell(fp_);
        if (size < 0) {
            throw std::runtime_error("ftell failed");
        }
        if (std::fseek(fp_, 0, SEEK_SET) != 0) {
            throw std::runtime_error("fseek set failed");
        }

        std::string out(static_cast<size_t>(size), '\0');
        size_t n = std::fread(out.data(), 1, out.size(), fp_);
        out.resize(n);
        return out;
    }

private:
    FILE* fp_ = nullptr;
};

int main() {
    return 0;
}
