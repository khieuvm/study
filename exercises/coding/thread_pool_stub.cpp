#include <condition_variable>
#include <functional>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>

class ThreadPool {
public:
    explicit ThreadPool(size_t worker_count) {
        // TODO: start workers
    }

    ~ThreadPool() {
        // TODO: stop and join
    }

    void submit(std::function<void()> task) {
        // TODO: push task and notify
    }

private:
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex mu_;
    std::condition_variable cv_;
    bool stop_ = false;
};

int main() {
    // TODO: basic test
    return 0;
}
