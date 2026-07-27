package hipstershop;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import hipstershop.Demo.Ad;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.Collection;
import java.util.List;
import org.junit.jupiter.api.Test;

// AdService keeps all of its logic in private static members, so these tests reach in via
// reflection rather than changing the production code's visibility just to make it testable.
class AdServiceTest {

  private static AdService getServiceInstance() throws ReflectiveOperationException {
    Method getInstance = AdService.class.getDeclaredMethod("getInstance");
    getInstance.setAccessible(true);
    return (AdService) getInstance.invoke(null);
  }

  private static Object invokePrivate(Object target, String methodName, Class<?>... paramTypes)
      throws ReflectiveOperationException {
    Method method = AdService.class.getDeclaredMethod(methodName, paramTypes);
    method.setAccessible(true);
    return method.invoke(target);
  }

  @Test
  void getAdsByCategory_returnsOnlyMatchingAds() throws Exception {
    AdService service = getServiceInstance();
    Method getAdsByCategory = AdService.class.getDeclaredMethod("getAdsByCategory", String.class);
    getAdsByCategory.setAccessible(true);

    @SuppressWarnings("unchecked")
    Collection<Ad> ads = (Collection<Ad>) getAdsByCategory.invoke(service, "hair");

    assertFalse(ads.isEmpty());
    assertTrue(ads.stream().allMatch(ad -> ad.getText().toLowerCase().contains("hairdryer")));
  }

  @Test
  void getAdsByCategory_returnsEmptyForUnknownCategory() throws Exception {
    AdService service = getServiceInstance();
    Method getAdsByCategory = AdService.class.getDeclaredMethod("getAdsByCategory", String.class);
    getAdsByCategory.setAccessible(true);

    @SuppressWarnings("unchecked")
    Collection<Ad> ads = (Collection<Ad>) getAdsByCategory.invoke(service, "does-not-exist");

    assertTrue(ads.isEmpty());
  }

  @Test
  void getRandomAds_returnsConfiguredNumberOfAds() throws Exception {
    AdService service = getServiceInstance();
    Field maxAdsField = AdService.class.getDeclaredField("MAX_ADS_TO_SERVE");
    maxAdsField.setAccessible(true);
    int maxAds = maxAdsField.getInt(null);

    @SuppressWarnings("unchecked")
    List<Ad> ads = (List<Ad>) invokePrivate(service, "getRandomAds");

    assertEquals(maxAds, ads.size());
  }
}
