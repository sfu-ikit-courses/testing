import unittest
import numpy as np
from myknn import MyKNN


class TestMyKNN(unittest.TestCase):
    def setUp(self):
        self.X = np.array([[0], [1], [2], [3]])
        self.y = np.array([0, 0, 1, 1])
        self.model = MyKNN(k=3)

    def tearDown(self):
        del self.model

    def test_fit_and_store(self):
        """Проверка: fit сохраняет данные и возвращает self"""
        ret = self.model.fit(self.X, self.y)
        self.assertIs(ret, self.model)
        X_copy, y_copy = self.model.get_train_copy()
        self.assertTrue(np.array_equal(X_copy, self.X))
        self.assertTrue(np.array_equal(y_copy, self.y))

    def test_predict_proba_range(self):
        """Вероятности в диапазоне [0,1]"""
        self.model.fit(self.X, self.y)
        probs = self.model.predict_proba(self.X)
        self.assertTrue(np.all(probs >= 0.0) and np.all(probs <= 1.0))

    def test_predict_binary(self):
        """Предсказания — 0 или 1"""
        self.model.fit(self.X, self.y)
        preds = self.model.predict(self.X)
        self.assertTrue(np.all(np.isin(preds, [0, 1])))

    def test_invalid_input_shapes(self):
        """Проверка реакции на некорректные размеры входных данных"""
        X_bad = np.array([[1, 2], [3, 4]])
        y_bad = np.array([0])
        with self.assertRaises(AssertionError):
            self.model.fit(X_bad, y_bad)

    def test_unfitted_predict_raises(self):
        """Если predict вызван до fit — ожидать ValueError"""
        with self.assertRaises(ValueError):
            self.model.predict(self.X)

    def test_different_k_values(self):
        """Проверка работы при разных k"""
        for k in [1, 2, 3, 4]:
            with self.subTest(k=k):
                m = MyKNN(k=k)
                m.fit(self.X, self.y)
                preds = m.predict(self.X)
                self.assertEqual(preds.shape[0], self.X.shape[0])

    def test_feature_mismatch(self):
        """Если при predict подать объект с другой размерностью признаков — AssertionError"""
        self.model.fit(self.X, self.y)
        X_wrong = np.array([[0, 1]])
        with self.assertRaises(AssertionError):
            self.model.predict_proba(X_wrong)

    def test_1d_input_reshaping(self):
        """Проверка: одномерный вход преобразуется в двумерный массив с одной строкой"""
        self.model.fit(self.X, self.y)
        X_1d = np.array([0])
        probs = self.model.predict_proba(X_1d)
        self.assertTrue(probs.shape == (1,))

    def test_invalid_ndim_input(self):
        """Если вход с недопустимым числом измерений — AssertionError"""
        self.model.fit(self.X, self.y)
        X_bad = np.array([[[1, 2]]])
        with self.assertRaises(AssertionError):
            self.model.predict_proba(X_bad)


if __name__ == "__main__":
    unittest.main()
