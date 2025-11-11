import numpy as np


class MyKNN(object):
    """
    Простейшая реализация K-Nearest Neighbors для бинарной классификации.
    Поддерживает fit, predict_proba, predict, валидацию входных данных.
    """

    def __init__(self, k=3):
        assert isinstance(k, int) and k >= 1, "k must be integer >= 1"
        self.k = k
        self._X = None
        self._y = None

    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        assert len(X) == len(y), "X and y must have same length"
        assert X.ndim == 2, "X must be 2D array"
        assert y.ndim == 1, "y must be 1D array"
        self._X = X.copy()
        self._y = y.copy()
        return self

    def _check_fitted(self):
        if self._X is None or self._y is None:
            raise ValueError("Model is not fitted yet")

    def _validate_X(self, X):
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        if X.ndim != 2:
            raise AssertionError("X must be 2D array")
        if X.shape[1] != self._X.shape[1]:
            raise AssertionError("Feature dimension mismatch")
        return X

    def _euclidean_distances(self, X):
        # X: [m, n], self._X: [l, n] -> distances [m, l]
        return np.sqrt(((X[:, None, :] - self._X[None, :, :]) ** 2).sum(axis=2))

    def predict_proba(self, X):
        """
        Возвращает вероятность принадлежности к классу 1 как доля соседей с y==1.
        """
        self._check_fitted()
        X = self._validate_X(X)
        dists = self._euclidean_distances(X)  # shape (m, l)
        probs = []
        for row in dists:
            nn_idx = np.argsort(row)[: self.k]
            neigh_labels = self._y[nn_idx]
            probs.append(np.mean(neigh_labels == 1))
        return np.array(probs)

    def predict(self, X, threshold=0.5):
        probs = self.predict_proba(X)
        return (probs >= threshold).astype(int)

    def get_train_copy(self):
        """Возвращает копию обучающего набора (для тестов — чтобы не отдавать ссылку на внутренние данные)."""
        self._check_fitted()
        return self._X.copy(), self._y.copy()
