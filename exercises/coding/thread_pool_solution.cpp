#include <condition_variable>
#include <functional>
#include <mutex>
#include <queue>
#include <stdexcept>
#include <thread>
#include <vector>

class ThreadPool {
public:
    explicit ThreadPool(size_t worker_count) {
        workers_.reserve(worker_count);
        for (size_t i = 0; i < worker_count; ++i) {
            workers_.emplace_back([this] {
                for (;;) {
                    std::function<void()> task;
                    {
                        std::unique_lock<std::mutex> lk(mu_);
                        cv_.wait(lk, [this] { return stop_ || !tasks_.empty(); });
                        if (stop_ && tasks_.empty()) {
                            return;
                        }
                        task = std::move(tasks_.front());
                        tasks_.pop();
                    }
                    task();
                }
            });
        }
    }

    ~ThreadPool() {
        {
            std::lock_guard<std::mutex> lg(mu_);
            stop_ = true;
        }
        cv_.notify_all();
        for (auto& t : workers_) {
            if (t.joinable()) {
                t.join();
            }
        }
    }

    void submit(std::function<void()> task) {
        {
            std::lock_guard<std::mutex> lg(mu_);
            if (stop_) {
                throw std::runtime_error("submit on stopped ThreadPool");
            }
            tasks_.push(std::move(task));
        }
        cv_.notify_one();
    }

private:
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex mu_;
    std::condition_variable cv_;
    bool stop_ = false;
};

int main() {
    return 0;
}
