# Exercise 03 - Modern C++ Refactor

## De bai
Code cu dung sentinel values va pointer null de bao loi.

## Yeu cau
1. Refactor ham tra ket qua bang `std::optional`.
2. Refactor union-tag thu cong bang `std::variant`.
3. Doi API `const std::string&` sang `std::string_view` o cho phu hop.
4. Liet ke bay life-time co the gap.

## Dap an goi y
- `optional<T>` khi co/khong co ket qua.
- `variant<A,B,C>` cho sum type an toan.
- `string_view` chi la view, khong so huu.

## Rubric
- Lua chon abstraction dung (0-4)
- Khong tao dangling view (0-3)
- Doc de hieu va maintain (0-3)
