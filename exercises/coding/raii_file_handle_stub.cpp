#include <cstdio>
#include <stdexcept>
#include <string>

class FileHandle {
public:
    explicit FileHandle(const std::string& path, const char* mode) {
        // TODO: open file, throw on error
    }

    ~FileHandle() noexcept {
        // TODO: close file safely
    }

    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    FileHandle(FileHandle&& other) noexcept {
        // TODO: move ownership
    }

    FileHandle& operator=(FileHandle&& other) noexcept {
        // TODO: move assign with self-check
        return *this;
    }

    std::string read_all() {
        // TODO: read full file content
        return {};
    }

private:
    FILE* fp_ = nullptr;
};

int main() {
    // TODO: quick manual test
    return 0;
}
