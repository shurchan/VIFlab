/*=====================
 -- Pixl --
 
 Created for CodeCanyon
 by FV iMAGINATION
 =====================*/

// Ad banners imports
#import <GoogleMobileAds/GoogleMobileAds.h>
#import <iAd/iAd.h>
#import <AudioToolbox/AudioToolbox.h>

#import "YCameraViewController.h"

#import <UIKit/UIKit.h>

UIImagePickerController *picker;

UIDocumentInteractionController *imageFile;
UIImage *combinedImage;



@interface ViewController : UIViewController
<
UIPopoverControllerDelegate,
UINavigationControllerDelegate,
UIImagePickerControllerDelegate,
UITabBarDelegate,
UIActionSheetDelegate,
UIScrollViewDelegate,
UIDocumentInteractionControllerDelegate,
GADBannerViewDelegate, ADBannerViewDelegate,
YCameraViewControllerDelegate
>

//Ad banners properties
@property (strong, nonatomic) ADBannerView *iAdBannerView;
@property (strong, nonatomic) GADBannerView *adMobBannerView;


// Views ==============
@property (weak, nonatomic) IBOutlet UIView *imageContainer;

@property (weak, nonatomic) IBOutlet UIScrollView *scrollView;
@property (weak, nonatomic) IBOutlet UIImageView *_imageView;
@property (weak, nonatomic) IBOutlet UIView *buttonsView;



@end
