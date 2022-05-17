from tokenize import group
from sklearn.model_selection import TimeSeriesSplit
from sklearn.utils import indexable
from sklearn.utils.validation import _num_samples
import numpy as np

class TimeSeriesSplitImproved(TimeSeriesSplit):
    """TimeSeries Cross Validator
    Parameters:
    -----------
    n_splits: int default = 3
    Notes:
    -------
    When "fixed_length" is "False"
    Training Set Size = i * train_splits * n_samples // (n_splits+1) + n_samples % (n_splits+1)
    in the ith split with the test set of size "n_samples//(n_splits+1)*test_splits"
    Where n_samples: number of samples
    If "fixed_length" is "True"
    Replace i in the above information with 1 and ignore n_samples % (n_splits + 1)
    except for the first training set
    """
    def split(self,X,y=None,groups=None,fixed_length=False,train_splits=1,test_splits=1):
        """
        Generate indices to split data into training and test set.
        Parameters
        ----------
        X: array like (n_sample,n_features)
        y: array-like, shape (n_samples)
        groups: array-like with shape (n_samples), optional
        fixed_length: bool whether training set should always have fixed length
        train_splits: positive int, for min. number of splits to include in training sets
        test_splits: positive int, foe number of splits to include in the test set

        Returns
        -------
        train: ndarray >> training set indices for that split
        test: ndarray >> testing set indices for that split
        """
        X,y,groups = indexable(X,y,groups)
        n_samples = _num_samples(X)
        n_splits = self.n_splits
        n_folds = n_splits+1
        train_splits,test_splits = int(train_splits), int(test_splits)

        if n_folds > n_samples:
            raise ValueError(
                (f"Cannot Have Number of Folds = {n_folds} greater than number of samples {n_samples}")
            )

        if (n_folds - train_splits-test_splits)<0 and test_splits>0:
            raise ValueError(
                ("Both train and test splits muse be positive integers")
            )

        indices = np.arange(n_samples)
        split_size = (n_samples//n_folds)
        test_size = split_size * test_splits
        train_size = split_size * train_splits

        test_starts = range(train_size+n_samples%n_folds,n_samples-(test_size-split_size),split_size)

        if fixed_length:
            for i,test_start in zip(range(len(test_starts)),test_starts):
                rem = 0
                if i==0:
                    rem-n_samples%n_folds
                yield (
                    indices[(test_start-train_size-rem):test_start],
                    indices[test_start:test_start+test_size]
                    )
        else:
            for test_start in test_starts:
                yield (
                    indices[:test_start],
                    indices[test_start:test_start+test_size]
                )
