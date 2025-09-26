from main import BooksCollector
import pytest

class TestBooksCollector:

    @pytest.mark.parametrize('book_name,expected', [
        ('К', True),                    
        ('К' * 40, True),                 
        ('Нормальное название', True),  
        ('', False),                    
        ('К' * 41, False)               
    ])
    def test_add_new_book_name_validation(self, book_name, expected):
    
        collector = BooksCollector()
        collector.add_new_book(book_name)
        
        if expected:
            assert book_name in collector.get_books_genre()
            assert collector.get_book_genre(book_name) == ''
        else:
            assert book_name not in collector.get_books_genre()

    
    def test_add_new_book_duplicate(self):
        
        collector = BooksCollector()
        collector.add_new_book('Дубликат')
        collector.add_new_book('Дубликат')
        assert len(collector.get_books_genre()) == 1
        assert list(collector.get_books_genre().keys()) == ['Дубликат']

    
    @pytest.mark.parametrize('genre,book_exists,expected', [
        ('Фантастика', True, True),     
        ('Комедии', True, True),        
        ('Несуществующий', True, False), 
        ('Фантастика', False, False)   
    ])
    def test_set_book_genre_validation(self, genre, book_exists, expected):
        
        collector = BooksCollector()
        book_name = 'Тестовая книга' if book_exists else 'Несуществующая'
        
        if book_exists:
            collector.add_new_book(book_name)
        
        collector.set_book_genre(book_name, genre)
        
        if expected:
            assert collector.get_book_genre(book_name) == genre
        else:
            if book_exists:
                assert collector.get_book_genre(book_name) == ''
            else:
                assert book_name not in collector.get_books_genre()

    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        
        collector.add_new_book('Фантастика книга')
        collector.add_new_book('Ужасы книга')
        collector.add_new_book('Еще фантастика')
        
        collector.set_book_genre('Фантастика книга', 'Фантастика')
        collector.set_book_genre('Ужасы книга', 'Ужасы')
        collector.set_book_genre('Еще фантастика', 'Фантастика')
        
        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        
        assert len(fantasy_books) == 2
        assert 'Фантастика книга' in fantasy_books
        assert 'Еще фантастика' in fantasy_books
        assert 'Ужасы книга' not in fantasy_books

    @pytest.mark.parametrize('genre,expected', [
        ('Ужасы', False),
        ('Детективы', False), 
        ('Фантастика', True),
        ('Комедии', True),
        ('Мультфильмы', True)
    ])
    def test_get_books_for_children(self, genre, expected):
        collector = BooksCollector()
        collector.add_new_book('Тестовая книга')
        collector.set_book_genre('Тестовая книга', genre)
        
        children_books = collector.get_books_for_children()
        
        if expected:
            assert 'Тестовая книга' in children_books
        else:
            assert 'Тестовая книга' not in children_books

    def test_favorites_workflow(self):
        collector = BooksCollector()
        collector.add_new_book('Тестовая книга')
        
        collector.add_book_in_favorites('Тестовая книга')
        assert 'Тестовая книга' in collector.get_list_of_favorites_books()
        assert len(collector.get_list_of_favorites_books()) == 1
        
        collector.add_book_in_favorites('Тестовая книга')
        assert len(collector.get_list_of_favorites_books()) == 1
        
        collector.delete_book_from_favorites('Тестовая книга')
        assert 'Тестовая книга' not in collector.get_list_of_favorites_books()
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_get_book_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        assert collector.get_book_genre('Книга') == ''
        
        collector.set_book_genre('Книга', 'Фантастика')
        assert collector.get_book_genre('Книга') == 'Фантастика'

    def test_get_books_genre(self):
        collector = BooksCollector()
        assert collector.get_books_genre() == {}
        
        collector.add_new_book('Книга1')
        collector.add_new_book('Книга2')
        books_dict = collector.get_books_genre()
        
        assert len(books_dict) == 2
        assert 'Книга1' in books_dict
        assert 'Книга2' in books_dict
        assert books_dict['Книга1'] == ''
        assert books_dict['Книга2'] == ''

    def test_add_nonexistent_book_to_favorites(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Несуществующая книга')
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_delete_nonexistent_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Существующая книга')
        collector.add_book_in_favorites('Существующая книга')
        
        collector.delete_book_from_favorites('Несуществующая книга')
        
        assert 'Существующая книга' in collector.get_list_of_favorites_books()
        
        