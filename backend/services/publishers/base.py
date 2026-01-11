class BasePublisher:
    """
    Abstract publisher class.
    All CMS publishers must follow this contract.
    """

    def publish(self, article):
        raise NotImplementedError(
            "Publisher must implement publish() method"
        )
